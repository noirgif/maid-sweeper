# Maid Sweeper for files

Instead of cleaning the unused files, it calls a maid to label them and sweep them under the rug accordingly.

However, the maid can practice Danshari given permission. For example, she can [sell your unused iPad for money](https://comic-days.com/episode/3269754496647364302).

## Feature

* Asyncio
* MongoDB
* Not scanning every single file inside code and program directories, saving time
    * Avoid accessing metadata
* Kyoufu

## Installation

1. Have Python 3.11 (as it used some fancy type hints that is incompatible with <3.11).
2. Install the requirements by running `pip install .`.

## Usage

1. Start a MongoDB instance.
2. Run `python maid.py tag D:\Study`, then you can find tagged entries in Database 'sweep_maid' Collection 'file_metadata'. Then it can be used for further processing.
3. Run `python maid.py sweep video,game rm -rf {}`, the maid is going to remove all 'video' or 'game' tagged files and directories.
    * As `fire` is used, it is about the best we can get, without custom deserializer 

## TO-DO

- [ ] Remove type hints
- [ ] Better readme
- [ ] Tag based on time
    * How does it affect other tags? If not why bother?
    * Maybe not tag, but just metadata
    * There will be IO cost
- [ ] Group similar named files
- [x] Automatically carry out actions based on the tags, like Dan, Sha and Ri, etc.
- [ ] Understand human language so they can toss away garbage

- [x] Better command line interface
    * have to escape {} for fire
- [ ] Optionally clean up the database after sweeping.
- [ ] Single line mode: do the tag, sweep, and clean up database entries with a single command.