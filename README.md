# File Sweeper

Instead of cleaning the unused files, it is outsourced to a maid to tag them and sweep them under the rug.

However, if allowed, this maid is also capable of Danshari (not yet). She will [sell your unused iPad for money](https://comic-days.com/episode/3269754496647364302).

## Feature

* Asyncio
* MongoDB
* Not scanning every single file inside code and program directories, saving time
* Scary

## How to use

0. Install the requirements by running `pip install -r requirements.txt`, as well as MongoDB.
1. Start a mongoDB instance
2. Run `python maid.py tag D:\Study`, then you can find tagged entries in Database 'sweep_maid' Collection 'file_metadata'.
3. Run `python maid.py sweep '["video","game"]' rm -rf {}`, the maid is going to remove all 'video' or 'game' tagged files and directories.
    * As `fire` is used, it is about the best we can get, without custom deserializer 

## TO-DO

[ ] Better readme

[ ] Tag based on time
    * How does it affect other tags? If not why bother?
    * Maybe not tag, but just metadata

[ ] Group similar named files

[x] Automatically carry out actions based on the tags, like Dan, Sha and Ri, etc.

[ ] Understand human language so they can toss away garbage

[ ] Better command line interface
    * the way of specifying tag list looks unwieldy

[ ] Performance
    * Seems to be bad inside a large directory