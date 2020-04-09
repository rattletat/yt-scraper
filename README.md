# YouTube Scraper
> A simple command utility to extract information from the YouTube API v3 for scientific purposes.

[![GitHub license](license-img)](license-url)

## About

This Python based command line utility enables the easy extraction of information from the YouTube API (Version 3). Currently, it only supports a small subset of functions of the API interface and focuses on extracting related videos from a given starting point.


## Installation

To install yt-scraper one can use [pip](pip-url):
```sh
sudo -H pip install yt-scraper
```

To update yt-scraper you can add the `--upgrade` flag:

```sh
sudo -H pip install --upgrade yt-scraper
```

## Usage example
### Commands
Currently, there is only one command: *search*

#### search
The search command starts a video search from a given starting point, such as a search term or a video itself.

For example the following command will return the first video when one searches for `cat`.

```sh
$ yt-scraper search term 'cat'
```
*VideoNode(videoId='0A2R27kCeD4', depth=0, rank=0, relatedVideos=('XewbmK0kmpI',))*

One can also provide a video id or a video url as a starting point, which is more interesting when used with the `--depth` option:

```sh
$ yt-scraper search id '0A2R27kCeD4' --depth 2
```
*VideoNode(videoId='0A2R27kCeD4', depth=0, rank=0, relatedVideos=('XewbmK0kmpI',))*
*VideoNode(videoId='XewbmK0kmpI', depth=1, rank=0, relatedVideos=('hJpfROXlaPc',))*
*VideoNode(videoId='hJpfROXlaPc', depth=2, rank=0, relatedVideos=('dElQqMWhDgA',))*

Additionally, one can specify the number of videos that should be returned on each level by using the `--number` option. For example the following command returns two related videos from a given video (specified by it's url) and then from each sibling only one related video:
```sh
$ yt-scraper search url 'https://www.youtube.com/watch?v=0A2R27kCeD4' --depth 1 --number 2 -number 1
```
*VideoNode(videoId='0A2R27kCeD4', depth=0, rank=0, relatedVideos=('XewbmK0kmpI', 'U5KLMeFK_UY'))*
*VideoNode(videoId='XewbmK0kmpI', depth=1, rank=0, relatedVideos=('hJpfROXlaPc',))*
*VideoNode(videoId='U5KLMeFK_UY', depth=1, rank=1, relatedVideos=('nFrb-C6I6Ps',))*

For the sake of brevity, you can shorten `--number` to `-n` and `--depth` to `-d`.

##### Options

| Search options    | Default    | Description                                                                             |
|-------------------|------------|-----------------------------------------------------------------------------------------|
| `-n`, `--number`  | 1          | Number of the videos fetched per level. Can be specified multiple times for each level. |
| `-d`, `--depth`   | 0          | Number of recursion steps to perform.                                                   |
| `-k`, `--api-key` | *Required* | The API key that should be used to query the YouTube API v3.                            |

### Global Options
Global options are specified before the command. For example, to get more output during the program execution, specify `-v` right after `yt-scraper`:

```sh
$ yt-scraper -v search term 'cat'
```

All global options:
| Global options        | Default           | Description                                                                                                       |
|-----------------------|-------------------|-------------------------------------------------------------------------------------------------------------------|
| `-c`, `--config-path` | *System-specific* | Specifies a configuration file. The default is system-specific. For details, see [configuration](#Configuration). |
| `-v`, `--verbose`     | False             | Shows more output during program execution.                                                                       |


### Configuration
Instead of repeatedly passing the same options to yt-scraper, one can specify these options in a `config.toml` file. These values will be used in all future queries as long as they are not get overwritten by actual command line options.

For example, to always use the API key `ABCDEFGH` and a search depth of 3, where on each level one video less is returned, just create following configuration file:

**config.toml**
```toml
api_key = "ABCDEFGH"
number = [ 4, 3, 2, 1 ]
depth = 3
```

Then put this file in your standard configuration folder. Typically this folder can be found at the following system-specific locations:

- Mac OS X: `~/Library/Application Support/YouTube Scraper`
- Unix: `~/.config/youtube-scraper`
- Windows: `C:\Users\<user>\AppData\Roaming\YouTube Scraper`

If the folder does not exist you may need to create it.


## Release History

* 0.2.6 
    - Added UNLICENSE
* 0.3.0
    - Uploaded to PyPI


## Roadmap

Every of these features is going to be a minor patch:

- [ ] Add node video data attributes, such as title and description.
- [ ] Add possibility to specify more than one API key to switch seamlessly.
- [ ] Add possibility to query more than 50 videos on one level.
- [ ] Add youtube-dl integration for downloading subtitles.
- [ ] Add a testing suite.
- [ ] Add export functionality to SQLlite or Pandas.
 

## Contributing
If you found a bug or have a suggestion, 
please don't hesitate to [file an issue](git-new-issue-url).

Contributions in any form are welcomed. 
I will accept pull-requests if they extent this program's functionality.

To set up the development environment, 
please install [Poetry](poetry-url) and run `poetry install` inside the project.
A test suite will be added soon.

In general, the contribution process is somehow like this:

1. Fork it (`git clone https://github.com/rattletat/yt-scraper`)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request


## Author
Michael Brauweiler

GitHub: [@rattletat](me-twitter-url)

Email: [rattletat@posteo.me](mailto:rattletat@posteo.me)


## License
This plugin is free and unemcumbered software released into the public domain. For more information, see the included [UNLICENSE](license-url) file.

<!-- Markdown link & img dfn's -->
[license-img]: https://img.shields.io/github/license/rattletat/yt-scraper?style=for-the-badge
[license-url]: https://github.com/rattletat/yt-scraper/blob/master/LICENSE
[pip-url]: https://pip.pypa.io/en/stable/
[git-new-issue-url]: https://github.com/rattletat/yt-scraper/issues/new
[poetry-url]: https://github.com/python-poetry/poetry
[me-github-url]: https://github.com/rattletat
[me-twitter-url]: https://twitter.com/m_brauweiler
[license-url]: https://github.com/rattletat/yt-scraper/blob/master/LICENSE
