# File Sweeper

Instead of cleaning the unused files, it is outsourced to a maid to tag them and sweep them under the rug.

However, if allowed, this maid is also capable of Danshari (not yet). She will [sell your unused iPad for money](https://comic-days.com/episode/3269754496647364302).

## Feature

* Asyncio
* MongoDB
* Not scanning every single file inside code and program directories, saving time
* Scary

## How to use

1. Start a mongoDB instance
2. Run `python main.py <path>`, then you can find tagged entries in Database 'sweep_maid' Collection 'file_metadata'.

## TO-DO

[ ] Better readme

[ ] Classify based on time

[ ] Group similar named files

[ ] Automatically carry out actions based on the tags, like moving them Dan, Sha and Ri, etc.

[ ] Understand human language so they can toss away garbage