# A `Doc` class, instantiated once for each document, holding its path,
# and original/converted data in various formats.

#{format: {tool-name: converted-text}}

#e.g. {'jpg': {'pdf2txt': <jpg-object>}}

# by using the to_target_format method, the document can be converted
# and stored in another format.

from importlib.metadata import metadata
import os
from PIL import Image
import string
from tqdm import tqdm
from tools.utils import *

class Doc:

   def __init__(self, input_filepaths, meta_name, tools):
      self.tools = tools

      # input_filepath is a LIST of filepaths (in case more files belong to the same document)
      self.input_filepaths = input_filepaths
      self.main_input_filepath = input_filepaths[0] # only used to detect filename and extension

      self.input_extension = os.path.splitext(self.main_input_filepath)[-1].lower().translate(str.maketrans('', '', string.punctuation))
      self.input_filename = os.path.basename(self.main_input_filepath).lower()
      
      self.txt_conversions = dict() # dict of {tool-name: converted-text} pairs

      self.data = dict() # dict of {target_format: {tool-name: converted-text}} e.g. {'jpg': {'pdf2txt': <jpg-object>}}
      self.meta_name = meta_name
      self.metadata = dict()

   def get_metadata(self, text):
      doc_dirpath = get_parent_dir(self.main_input_filepath)
      meta_path = os.path.join(doc_dirpath,self.meta_name)
      metadata_exists_Q = os.path.isfile(meta_path)
      if metadata_exists_Q:
         print('Reading existing metadata for {0}.'.format(self.input_filename))
         with open(meta_path) as f:
            metadata = json.load(f)
         dbg(metadata)
         return metadata
      else:
         print('Generating metadata.')
         prep_text,_ = prep_and_tokenise(self.data['txt']['pytesseract_ocr'])
         self.metadata['lang_codes'] = get_langs(prep_text)
         self.metadata['emb_txt'] = get_emb_txt(prep_text)
         lang_codes = self.metadata['lang_codes']
         emb_txt = self.metadata['emb_txt']
         return dict(lang_codes=lang_codes,
                  emb_txt=emb_txt)

   ## doc conversion img<>pdf
   def to_target_format(self, target_format, tool_name = None):
      """target_format can be pdf, png"""
      #selected_tool_name = tool_name
      global selected_tool_name
      data_selection = self.data.get(target_format)      
      if data_selection:                           # if at least an instance of (converted/original) data is already stored for given target_format...
         if not tool_name:
            converted_data = data_selection[0]     # ...take the first instance available...
         else:
            converted_data = data_selection[tool_name]  #...unless a preferred conversion tool was selected
         return converted_data
      else: # if the requested extension has no instances, add an empty instance target_format:{}
         self.data[target_format] = dict()
         
      # if requested target_format matches filepath extension, open the document and store it as an object
      if target_format == 'pdf':
         if self.data['pdf']:
            return
         if self.is_pdf():
            # open all files for the given document...
            pdf_objects = []
            for pdf_path in self.input_filepaths:
               with open(pdf_path, 'rb') as file:
                  pdf_objects.append(file)
            converted_data = pdf_objects
            
            self.data[target_format]['original'] = converted_data # ...and store original data in self.data
            
         elif self.is_png(): # if requested target_format does NOT match filepath extension, convert it
            
            tool_selection = self.tools[('png','pdf')] # this gives a dict of suitable tools
            
            if tool_name is None:
               selected_tool_name = list(tool_selection)[0]
               conversion_tool = tool_selection[selected_tool_name] # take first available tool if no tool was specified
            else:
               selected_tool_name=tool_name
               conversion_tool = tool_selection[selected_tool_name] # assign tool based on tool name
                        
            png_objects = None # TODO open files...
            
            converted_data = conversion_tool( # ...apply conversion tool on them...
               png_objects
            )

            self.data[target_format][selected_tool_name] = converted_data # ...and store the converted data
         else:
            print('Error: source format {0} is nor accepted'.format(self.input_extension))
            return
      
      # if requested target_format matches filepath extension, open the document and store it as an object
      elif target_format == "png":
         if self.data['png']:
            return
         if self.is_png():   
            # open all files for the given document...
            converted_data = [
               Image.open(image_path) for image_path in self.input_filepaths
               ]
               
            self.data[target_format]['original'] = converted_data # ... and store original data in self.data

         elif self.is_pdf():
            tool_selection = self.tools[('pdf','png')] # this gives a dict of suitable tools
            if tool_name is None:
               selected_tool_name = list(tool_selection)[0]
               conversion_tool = tool_selection[selected_tool_name] # take first available tool if no tool was specified
            else:
               selected_tool_name=tool_name
               conversion_tool = tool_selection[selected_tool_name] # assign tool based on tool name
                        
            pdf_filepath = [ # open files...
               path for path in self.input_filepaths if path.endswith('.pdf')
            ][0]
            
            converted_data = conversion_tool( # ...apply conversion tool on them...
               pdf_filepath
            )
            self.data[target_format][selected_tool_name] = converted_data # ...and store the converted data
            
            #print('self.data[{0}][{1}]:{2}'.format(target_format,selected_tool_name,self.data[target_format][selected_tool_name]))
            
         else:
            #print('Error: source format {0} is nor accepted'.format(self.input_extension))
            return
      else:
         #print('Error: target_format {0} is nor accepted'.format(target_format))
         return
      
      #print('self.data[{0}][{1}]:{2}'.format(target_format,selected_tool_name,self.data[target_format][selected_tool_name]))
      return 
      
   ## check extension
   def is_pdf(self):
      return self.input_extension.lower() == 'pdf'
   def is_png(self):
      return self.input_extension.lower() == 'png'

   ## save output txt
   def save_txt_conversion(self, tool_name, doc_path, overwrite=False):
      # define output filepath
      output_file_path = os.path.join(doc_path,tool_name,str(self.input_filename)+'.txt')
      if overwrite == False and os.path.isfile(output_file_path): # if overwriting is not allowed and file already exists...
         return      # ...do not save
      
      # save txt in chosen dir
      os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
      with open(output_file_path, 'w+') as f:
         try:
            f.write(self.txt_conversions[tool_name])
         except:
            print('couldn\'t write txt file for',self.main_input_filepath)
      return
   
   def save_all_txt_conversions(self, doc_path, overwrite):
      for tool in self.txt_conversions.keys():
         self.save_txt_conversion(tool, doc_path, overwrite)

class TxtConverter:
   def __init__(self, tools):
      #self.available_functions = {str(f):f for f in globals().values() if type(f) == types.FunctionType}
      self.tools = tools
   # select tool and convert
   def convert_to_txt(self,
                     doc,
                     input_formats=['pdf','png'],
                     tool_names = None):

      output_format = 'txt'
      tool_selection = {}
      for input_format in input_formats:
         tool_selection.update(self.tools[(input_format, output_format)]) # this adds tools given the required formats
      if isinstance(tool_names, str):
         tool_names = [tool_names]

      if tool_names is None: # use all the conversion tools
         tool_names = tool_selection.keys()
      
      print('tool_selection.keys()',tool_selection.keys())
      print('tool_names',tool_names)
      selected_tools = {}
      for tool_name in tool_names:
         selected_tools[tool_name] = tool_selection[tool_name]

      extracted_texts = dict()
      for t_name in tqdm(tool_names):
         req_ext = ter[t_name]      # extract input format of tool
         doc_ext = doc.data[req_ext]
         #TODO: if doc_ext is empty: convert
         
         first_tool_name = list(doc_ext.keys())[0]
         pdf_filepath = doc.main_input_filepath      # get path from doc # TODO: trat multiple pdfs per document
         extracted_texts[t_name]= selected_tools[t_name](pdf_filepath)  # pass it to tool

      #store in doc.txt_conversions
      doc.txt_conversions.update(extracted_texts) # join the dictionaires
      
      # store in doc.data
      if not doc.data.get('txt'):
         doc.data['txt'] = dict()
      
      doc.data['txt'].update(extracted_texts) # join the dictionaires