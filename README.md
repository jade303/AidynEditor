# AidynEditor
An editor for Aidyn Chronicles - The First Mage

Party edits are new game only or until the party member joins you.

Some spells are pretty glitchy, like Wraith Touch or Escape. Be cautious.

If you want an exe file:
<pre>
1. Install Python
2. Open command prompt (or equivalent)
3. enter: pip install pyinstaller
4. navigate to the folder that contains AidynEditor
  (or open folder and right click in an empty area and select 'open command prompt' (or equivalent)
5a. if you want one file:
      from command prompt:
        pyinstaller --noconsole --onefile AidynEditor.py
5b. if one folder is fine for you:
      from command prompt:
        pyinstaller --noconsole AidynEditor.py
6. One file or one folder options are found in the dist folder that is created
</pre>

TODO: item, drop, and trainer edits.
