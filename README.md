## IndexCrawler

I wrote a script to download entire folders from Apache's "Index of" listings.

It downloads the given file, or a listing. If it's a listing, it'll recursively
go in and download all files in it.

It stores everything in `$target_folder`, in a directory structure similar to the
URL. If URL is `something.com/Films/2001/Movie.mkv`, It'll be stored at
`$target_folder/Films/2001/Movie.mkv`.

It also checks in target folder for every file before downloading it. If the
file is there, it's not downloaded. So you can Ctrl-C any time and continue
later, without worrying about downloading anything twice.

### Installation:

- Install axel. Else you'll have to write a replacement for axelFile. 
Just make sure you follow the same pattern.

- Download the file `crawler.py`.

**It runs on python3**. Sorry :P

- Run: 

`python3 crawler.py URL /target/folder`


### Variables

- `tmp_folder` is a folder preferably on your main hard disk, not on a USB drive. 
I noticed that downloading is significantly slower if OS has to write to a
mounted folder.
