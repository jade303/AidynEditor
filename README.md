# AidynEditor
An editor for Aidyn Chronicles - The First Mage

Party edits are new game only or until the party member joins you.

Wraith Touch is very glitchy. The only way I've gotten it to work on a character that isn't a Wraith 
is by changing the battle model to that of the Wraith and using Wraith Touch. Otherwise the game crashes.

<pre>
If you want an exe file:
1. Install Python
2. Open command prompt (or equivalent)
3. enter: pip install pyinstaller
4. navigate to the folder that contains AidynEditor
  (or open folder and right click in an empty area and select 'open command prompt' (or equivalent)
5. if you want one file:
      from command prompt:
        pyinstaller --noconsole --onefile AidynEditor.py
6. if one folder is fine for you:
      from command prompt:
        pyinstaller --noconsole AidynEditor.py
7. One file or one folder options are found in the dist folder that is created
</pre>

TODO: item edits.
