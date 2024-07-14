# TBD
# You will need audacity installed for these steps
# Following these steps https://manual.audacityteam.org/man/scripting.html
# To enable external scripts to run on audacity

import os
import sys
import json
import uuid

class Audacity():
  def do(self,command):
      """Send one command, and return the response."""
      print(f"running command {command}")
      self.__send_command(command)
      response = self.__get_response()
      # print("Rcvd: <<< \n" + response)
      return response

  def __init__(self):
    self.__setup_audacity_pipes()
    self.__setup_open_files()
    self.__quick_test()

  def __setup_audacity_pipes(self):
    if sys.platform == 'win32':
        print("pipe-test.py, running on windows")
        self.TONAME = '\\\\.\\pipe\\ToSrvPipe'
        self.FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
        self.EOL = '\r\n\0'
    else:
        print("pipe-test.py, running on linux or mac")
        self.TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
        self.FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
        self.EOL = '\n'

    print("Write to  \"" + self.TONAME +"\"")
    if not os.path.exists(self.TONAME):
        print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
        sys.exit()

    print("Read from \"" + self.FROMNAME +"\"")
    if not os.path.exists(self.FROMNAME):
        print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
        sys.exit()

    print("-- Both pipes exist.  Good.")

  def __open_files_to_write(self):
    self.TOFILE = open(self.TONAME, 'w')
    print("-- File to write to has been opened")
  
  def __open_files_to_read(self):
    self.FROMFILE = open(self.FROMNAME, 'rt')
    print("-- File to read from has been opened")
  
  def __setup_open_files(self):
    self.__open_files_to_write()
    self.__open_files_to_read()

  def __send_command(self, command):
      """Send a single command."""
      print("Send: >>> \n"+command)
      self.TOFILE.write(command + self.EOL)
      self.TOFILE.flush()

  def __get_response(self):
      """Return the command response."""
      result = ''
      line = ''
      while True:
          result += line
          line = self.FROMFILE.readline()
          if line == '\n' and len(result) > 0:
              break
      return result
  
  def __quick_test(self):
      """Example list of commands."""
      self.do('Help: Command=Help')
      self.do('Help: Command="GetInfo"')
      #do_command('SetPreference: Name=GUI/Theme Value=classic Reload=1')




def label_sounds(audacity: Audacity, file_path: str, out_dir: str):
  # clear audacity project
  audacity.do('SelectAll')
  audacity.do('RemoveTracks')

  # Open the file
  audacity.do(f'Import2: Filename="{file_path}"')

  # ISILDUR, TOSS THE RING INTO THE VOLCANO
  # Label the sounds
  audacity.do('LabelSounds: threshold=-37.0 sil-dur=0.350 snd-dur=2 pre-offset=0.3 post-offset=0.3 text="py-voice-clone-label"')

  # Get label info
  labels = audacity.do('GetInfo: Type=Labels Format=JSON')

  # Parse returned string
  labels_arr = labels.split('\n')
  # Need to pop the last 2 elements, they're trash
  labels_arr.pop()
  labels_arr.pop()
  
  labels = "".join(labels_arr)
  labels = json.loads(labels)

  audacity.do('SelNextClip')

  # Extract labeled audio
  for (label_start, label_end, label_name) in labels[0][1]:
    print(f's: {label_start}, e: {label_end}, n: {label_name}')
    audacity.do(f'Select: Start={label_start} End={label_end}')
    audacity.do(f'Export2: Filename={out_dir}/out/labeled_audio/{uuid.uuid4()}.wav')

