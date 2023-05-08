# Maid Sweeper for files

Instead of cleaning the unused files, it calls a maid to label them and sweep them under the rug accordingly.

However, the maid can practice Danshari given permission. For example, she can [sell your unused iPad for money](https://comic-days.com/episode/3269754496647364302).

Like Toki, she has two modes:

`tag`: Label the files/directories automatically, based on their types and names.

- code projects and application directories are labeled, and their children are not scanned
- others are labeled based on the extensions

`sweep`: Carry out actions based on the labels`.

## Feature

* AsyncIO, so all operations are in parallel
* MongoDB for fast indexing
* Save time by not scanning every single file inside code and program directories and not checking the metadata
* Kyoufu

## Installation

1. Have Python 3.10.
2. Install by running `pip install maid-sweeper`.

## Usage

1. Start a MongoDB instance.
2. Run `maid-sweeper tag D:\Study`, then you can find tagged entries in the database. Sweeping works on all directories tagged.
3. Run `maid-sweeper sweep -t video game -x del \q \f {}`, and the maid is going to remove all 'video' or 'game' tagged files and directories.
    * Any other commands is OK as well
    * By default the maid will do a sweep -- remove all those files. Kyoufu!

## Ideas

- Multithreading
- Remove type hints
- Tags based on time
    * How does it affect other tags? If not why bother?
    * Maybe not tag, but just metadata
    * There will be IO cost
- Group similarly named files: 01.jpg, 02.jpg, etc.
- Understand human language so they can toss away garbage
- Optionally clean up the database after sweeping.
- Single line mode: do the tag, sweep, and clean up database entries with a single command.
- Allow users to specify tags