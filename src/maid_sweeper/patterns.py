# Files that determines the type of its parent directory
import re

TYPICAL_FILES_LIST : dict[str, list[str]]= {
    "code-project": [
        r'^\.git$',
        r'^\.hg$',
        r'^\.svn$',
        r'^\.bzr$',
        r'^\.gitignore$',
        r'^\.gitattributes$',
        r'^\.hgignore$',
        r'^\.npmignore$',
        r'^\.dockerignore$',
        r'^package\.json$',
        r'^yarn\.lock$',
        r'^Gemfile$',
        r'^Gemfile\.lock$',
        r'^Pipfile$',
        r'^Pipfile\.lock$',
        r'^requirements\.txt$',
        r'^go\.mod$',
        r'^go\.sum$',
        r'^Cargo\.toml$',
        r'^Cargo\.lock$',
        r'^composer\.json$',
        r'^composer\.lock$',
        r'^.*csproj$',
        r'^.*fsproj$',
        r'^.*vbproj$',
        r'^gradlew$',
        r'^gradlew\.bat$',
        r'^build\.gradle$',
        r'^pom\.xml$',
        r'^Makefile$',
        r'^CMakeLists\.txt$',
        r'^setup\.py$',
        r'^Rakefile$',
        r'^Gruntfile\.js$',
        r'^gulpfile\.js$',
        r'^webpack\.config\.js$',
        r'^rollup\.config\.js$',
        r'^\.travis\.yml$',
        r'^\.circleci$',
        r'^\.github$',
        r'^Dockerfile$',
        r'^Vagrantfile$',
        r'^\.env$',
        r'^\.editorconfig$',
        r'^\.prettierrc$',
        r'^\.eslintrc$',
        r'^tsconfig\.json$',
        r'^\.vscode$',
        r'^.*\.tex$',
        r'README(\.md)?$',
        r'^LICENSE$',
    ],
    "game": [
        r'^Game.exe$',  # RPG Maker, or Wolf
        r'^.*\.xp3$',  # KiriKiri
        r'^Game.rgss3a$',  # RPG Maker
        r'^BGI.exe$',  # BGI
        r'^.*\.arc$',  # also BGI
        r'^save$',  # some text games with local saves
        r'^savedata$',  # ditto
        r'^.*\.dat$',
        r'^.*\.sav$',
        r'^.*\.rpgsave$',
        r'^.*\.mpk$',
        r'^.*\.pak$',  # some kirikiri games
        r'^Ron2.exe$',  # RON
        r'^.*\.rpyc$',  # Ren'Py
        r'^renpy$',  # ditto
        r'^tyrano$',  # TyranoScript
        r'^UnityPlayer.dll$',  # Unity
        r'^BGM$',  # some games, like CrackleCradle
        r'^root\.pfs',  # Artemis Engine
        r'^.*_Data$',  # Unity
        r'^README\.txt$',  # some games
    ],
    "software": [
        r'^.*\.dll$',
        r'^Unins\w*\.exe$',
    ],
    "album": [
        r'^.*\.cue$',
    ],
}

TYPICAL_FILES_RE : dict[str, re.Pattern]= {}
for k, v in TYPICAL_FILES_LIST.items():
    TYPICAL_FILES_RE[k] = re.compile('|'.join(v), re.IGNORECASE)

EXTENSIONS = {
    # Text formats
    "text": set(['txt', 'md', 'rtf', 'tex', 'doc', 'docx', 'odt', 'pdf']),

    # Image formats
    "image": set(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'svg', 'webp', 'ico', 'heic']),

    # Audio formats
    "audio": set(['mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a', 'wma']),

    # Video formats
    "video": set(['mp4', 'mkv', 'avi', 'mov', 'wmv', 'flv', 'webm', 'm4v', 'mpg', 'mpeg']),

    # Compressed formats
    "compressed": set(['zip', 'rar', 'tar', 'gz', 'bz2', '7z', 'xz', 'iso']),

    # Code and markup formats
    "source-code": set(['py', 'js', 'html', 'css', 'php', 'java', 'cpp', 'c', 'cs', 'go', 'rb', 'xml', 'json', 'yml', 'yaml']),

    # Database formats
    "database": set(['sql', 'db', 'sqlite', 'sqlite3', 'mdb', 'accdb']),

    # Spreadsheet formats
    "spreadsheet": set(['xls', 'xlsx', 'ods', 'csv']),

    # Presentation formats
    "presentation": set(['ppt', 'pptx', 'odp']),

    # Executable formats
    "executable": set(['exe', 'bat', 'sh', 'app', 'msi', 'apk', 'jar']),

    # Font formats
    "font": set(['ttf', 'otf', 'woff', 'woff2', 'eot', 'fon']),

    # eBook formats
    "book": set(['epub', 'mobi', 'azw', 'azw3', 'djvu']),
}

FILENAMES: list[tuple[list[str], str]] = [
    # ArXiv paper
    (["arxiv"], r'^\d{4}\.\d{4,5}\.pdf$'),

    # Game Software
    (["game", "dmm"], r'^[a-z]{4,5}_\d{4,5}\.exe$'),

    # Media Software
    (["media", "DLsite"], r'^(RJ|VJ)\d{6,8}\.zip$'),

    # Book
    (["book", "DLsite"], r'^BJ\d{6,8}\.zip$'),
]

FILENAMES_RE: list[tuple[list[str], re.Pattern]] = []
for tags, pattern in FILENAMES:
    FILENAMES_RE.append((tags, re.compile(pattern)))

# Synonym for tags, used when sweeping
SYNONYMS = {
    "document": ["text", "spreadsheet", "presentation", "pdf", "book"],
    "media": ["image", "audio", "video", "game"],
    "archive": ["compressed", "database"],
    "code": ["source-code", "code-project"],
}