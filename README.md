# Lockmynotes

A minimalistic password-locked note editor written in Python.

## Features

* AES-256 Encryption.
* ECC via Reed-Solomon code. This means that your file will be automatically recovered if it somehow gets corrupted.  
  Note: recovery is possible only after a limited degree of corruption.
* Fully self-contained: you can review every line of the source code (there aren't many).
* Runs on Linux and Windows, should run on other OSes as well.
* Tested.

## How to use it

Ensure that your system has python 2.x. Linux distros usually have it by default, while on Windows you will have to install it manually.

Download the git repo as a zip archive and unpack it, or clone the repo:
`git clone https://github.com/crystalline/lockmynotes; cd lockmynotes`

Run the program
`python notepad.py`

You can make notepad.py an executable file and/or send a shortcut of it to your desktop

## Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


