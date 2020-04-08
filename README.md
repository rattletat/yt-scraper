fetch-yt.py

`-q --query STRING` 
Text that is used for the search on YouTube. Needed

`-o --output`
Specifies the output file.
**Default:** ``data/result.sql``

`-n --number INTEGER (ARRAY)`
Number of videos fetched per level. 
If an array is provided, the i-th element equals 
the number of videos fetched on the i-th level.
**Default**: 10

`-l --levels INTEGER`
Number of recursion steps per video.
**Default**: 1

`-v --verbose`
Print more information to output.


## Known Issues

- The `number` parameter is restricted to maximal 50. This can be fixed in the
future by iterating through result pages.
