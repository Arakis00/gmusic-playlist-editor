from musicFunctions import *
from gmusicapi import Mobileclient
from StringIO import StringIO
from Tkinter import *
import Tkinter as tk

global libraryListBox, playlistListBox
playlistList = list() #set to a blank list

class DialogueBox:
    '''Provides a popup input box for the user to input a playlist name when saving or select a playlist when loading'''
    def __init__(self, parent, saveOrPlaylist):
        '''Create dialogue box, saveOrLoad will either contain the string 'save' when performing a save or a list of playlists to load'''
        top = self.top = Toplevel(parent)
        self.saveOrPlaylist = saveOrPlaylist #set as a class attribute so it can be accessed in OK Button command
        
        #determine which type of dialogue box to show depending on whether saving or loading a playlist
        if saveOrPlaylist == "save": #show entry to enter playlist name
            Label(top, text="Enter Name to Save As:").pack()
            self.e = Entry(top)
            self.e.pack(padx=5)
        else: #a list was passed, so show and populate listbox to select playlist from
            Label(top, text="Select a Playlist to Load:").pack()
            self.l = Listbox(top)
            self.l.pack(padx=5)
            #place playlist listing into popup listbox
            for plist in saveOrPlaylist:
                self.l.insert(END, plist['name'])
        
        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)
        
    def ok(self):
        '''Save input when OK button is hit in dialogue box'''
        if self.saveOrPlaylist == "save": #save operation, save the name entered into the entry dialogue
            self.playlistSaveName = self.e.get() #class attribute to save the string that was input
        else: #load operation, save the listbox selection
            self.playlistLoadIndex = self.l.curselection()[0] #NOTE - curselection returns a tuple, so obtain first index element
        self.top.destroy()

        
def findArtist(search, libraryList):
    '''Search the library for a given artist and show matches'''
    if (search.get() == ''): #search box is blank, so show full library
        libraryList[:] = getLibrary()
    else: #search box has a value, show search results
        libraryList[:] = searchLibrary(search.get())
    #clear current listbox and place library listing into library Listbox (left)
    libraryListbox.delete(0, END)
    for track in libraryList:
        libraryListbox.insert(END, (track['artist'] + " - " + track['title']))

def playlistAdd(selectionIndex, libraryList):
    '''Add the song selected in the libraryListBox to the playlist that will be shown in the playlistListbox'''
    #add currently selected libraryList object to the end of the current playlist
    playlistList.append(libraryList[selectionIndex])
    #add the new object to the playlistListbox
    playlistListbox.insert(END, libraryList[selectionIndex]['artist'] + " - " + libraryList[selectionIndex]['title'])
    
def playlistRemove(selectionIndex):
    '''Remove the song selected in the playlistListbox from the playlist'''
    #remove selected item from list
    playlistList.pop(selectionIndex)
    #update the playlistListbox
    playlistListbox.delete(selectionIndex)
    
def playlistSave():
    '''Allow the user to save the current playlist'''
    #open dialogue window to get name to save as
    d = DialogueBox(main, "save")
    main.wait_window(d.top)
    #save playlist
    savePlaylist(playlistList, d.playlistSaveName)
    
def playlistLoad():
    '''Allow the user to select a playlist to load'''
    #get a listing of all playlists
    playlists = getPlaylists()
    #open dialogue window to show a listing of available playlists to load
    l = DialogueBox(main, playlists)
    main.wait_window(l.top)
    #load playlist songs into its' listbox
    playlistList[:] = playlists[l.playlistLoadIndex]['tracks']
    playlistListbox.delete(0, END)
    fullLibraryList = getLibrary() #create a full library listing to compare track id's and get artist/title information, since the API playlist loading dictionaries does not contain that information
    i = 0 #index counter
    
    #replacing playlist dictionary listings with the library listing format that is compatible with the rest of the program and showing in the playlistListbox.
    for track in playlistList:
        for libTrack in fullLibraryList:
            if track['trackId'] == libTrack['id']:
                playlistList[i] = libTrack
                playlistListbox.insert(END, (playlistList[i]['artist'] + " - " + playlistList[i]['title']))
        i += 1
    
#create main window    
main = tk.Tk()
main.title("Google Music - Playlists")
main.geometry("800x600")
#create menu bar
menuBar = tk.Menu(main)
fileMenu = tk.Menu(menuBar, tearoff=0)
fileMenu.add_command(label="Open Playlist", command=playlistLoad)
fileMenu.add_command(label="Save Playlist", command=playlistSave)
menuBar.add_cascade(label="File", menu=fileMenu)
main.config(menu=menuBar)

#get full library to show in listbox at startup
libraryList = getLibrary()

#create GUI objects
searchEntry = tk.Entry(main)
searchButton = tk.Button(main, text="Find Artist", command=lambda:findArtist(searchEntry, libraryList))
libraryListbox = Listbox(main, height=35, width=40)
addButton = tk.Button(main, text="Add =>", command=lambda:playlistAdd(libraryListbox.curselection()[0], libraryList)) #note - curselection returns a tuple so get first element(index 0)
playlistListbox = Listbox(main, height=35, width=40)
removeButton = tk.Button(main, text="<= Remove", command=lambda:playlistRemove(playlistListbox.curselection()[0]))

#place GUI objects
searchEntry.pack(side=tk.TOP)
searchButton.pack(side=tk.TOP)
libraryListbox.pack(side=tk.LEFT)
addButton.pack(side=tk.LEFT)
playlistListbox.pack(side=tk.RIGHT)
removeButton.pack(side=tk.RIGHT)

#place library listing into library Listbox (left)
for track in libraryList:
    libraryListbox.insert(END, (track['artist'] + " - " + track['title']))

main.mainloop()