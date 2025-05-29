// Game configuration
const WORD_LISTS = {
    5: ['ABOUT', 'ABOVE', 'ABUSE', 'ACTOR', 'ACUTE', 'ADMIT', 'ADOPT', 'ADULT', 'AFTER', 'AGAIN', 'AGENT', 'AGREE', 'AHEAD', 'ALARM', 'ALBUM', 'ALERT', 'ALIEN', 'ALIGN', 'ALIKE', 'ALIVE', 'ALLOW', 'ALONE', 'ALONG', 'ALTER', 'ANGEL', 'ANGER', 'ANGLE', 'ANGRY', 'APART', 'APPLE', 'APPLY', 'ARENA', 'ARGUE', 'ARISE', 'ARRAY', 'ASIDE', 'ASSET', 'AVOID', 'AWAKE', 'AWARD', 'AWARE', 'BADLY', 'BAKER', 'BASES', 'BASIC', 'BEACH', 'BEGAN', 'BEGIN', 'BEING', 'BELOW', 'BENCH', 'BILLY', 'BIRTH', 'BLACK', 'BLAME', 'BLANK', 'BLAST', 'BLIND', 'BLOCK', 'BLOOD', 'BOARD', 'BOAST', 'BOBBY', 'BOOTH', 'BOUND', 'BRAIN', 'BRAND', 'BRAVE', 'BREAD', 'BREAK', 'BREED', 'BRIEF', 'BRING', 'BROAD', 'BROKE', 'BROWN', 'BUILD', 'BUILT', 'BUYER', 'CABLE', 'CALIF', 'CARRY', 'CATCH', 'CAUSE', 'CHAIN', 'CHAIR', 'CHAOS', 'CHARM', 'CHART', 'CHASE', 'CHEAP', 'CHECK', 'CHEST', 'CHIEF', 'CHILD', 'CHINA', 'CHOSE', 'CIVIC', 'CIVIL', 'CLAIM', 'CLASS', 'CLEAN', 'CLEAR', 'CLICK', 'CLIMB', 'CLOCK', 'CLOSE', 'CLOUD', 'COACH', 'COAST', 'COULD', 'COUNT', 'COURT', 'COVER', 'CRAFT', 'CRASH', 'CRAZY', 'CREAM', 'CRIME', 'CROSS', 'CROWD', 'CROWN', 'CRUDE', 'CURVE', 'CYCLE', 'DAILY', 'DANCE', 'DATED', 'DEALT', 'DEATH', 'DEBUT', 'DELAY', 'DEPTH', 'DOING', 'DOUBT', 'DOZEN', 'DRAFT', 'DRAMA', 'DRANK', 'DRAWN', 'DREAM', 'DRESS', 'DRILL', 'DRINK', 'DRIVE', 'DROVE', 'DYING', 'EAGER', 'EARLY', 'EARTH', 'EIGHT', 'ELITE', 'EMPTY', 'ENEMY', 'ENJOY', 'ENTER', 'ENTRY', 'EQUAL', 'ERROR', 'EVENT', 'EVERY', 'EXACT', 'EXIST', 'EXTRA', 'FAITH', 'FALSE', 'FAULT', 'FIBER', 'FIELD', 'FIFTH', 'FIFTY', 'FIGHT', 'FINAL', 'FIRST', 'FIXED', 'FLASH', 'FLEET', 'FLOOR', 'FLUID', 'FOCUS', 'FORCE', 'FORTH', 'FORTY', 'FORUM', 'FOUND', 'FRAME', 'FRANK', 'FRAUD', 'FRESH', 'FRONT', 'FRUIT', 'FULLY', 'FUNNY', 'GIANT', 'GIVEN', 'GLASS', 'GLOBE', 'GOING', 'GRACE', 'GRADE', 'GRAND', 'GRANT', 'GRASS', 'GRAVE', 'GREAT', 'GREEN', 'GROSS', 'GROUP', 'GROWN', 'GUARD', 'GUESS', 'GUEST', 'GUIDE', 'HAPPY', 'HARRY', 'HEART', 'HEAVY', 'HENCE', 'HENRY', 'HORSE', 'HOTEL', 'HOUSE', 'HUMAN', 'IDEAL', 'IMAGE', 'INDEX', 'INNER', 'INPUT', 'ISSUE', 'JAPAN', 'JIMMY', 'JOINT', 'JONES', 'JUDGE', 'KNOWN', 'LABEL', 'LARGE', 'LASER', 'LATER', 'LAUGH', 'LAYER', 'LEARN', 'LEASE', 'LEAST', 'LEAVE', 'LEGAL', 'LEVEL', 'LEWIS', 'LIGHT', 'LIMIT', 'LIVED', 'LOCAL', 'LOOSE', 'LOWER', 'LUCKY', 'LUNCH', 'LYING', 'MAGIC', 'MAJOR', 'MAKER', 'MARCH', 'MARIA', 'MATCH', 'MAYBE', 'MAYOR', 'MEANT', 'MEDIA', 'METAL', 'MIGHT', 'MINOR', 'MINUS', 'MIXED', 'MODEL', 'MONEY', 'MONTH', 'MORAL', 'MOTOR', 'MOUNT', 'MOUSE', 'MOUTH', 'MOVED', 'MOVIE', 'MUSIC', 'NEEDS', 'NEVER', 'NEWLY', 'NIGHT', 'NOISE', 'NORTH', 'NOTED', 'NOVEL', 'NURSE', 'OCCUR', 'OCEAN', 'OFFER', 'OFTEN', 'ORDER', 'OTHER', 'OUGHT', 'PAINT', 'PANEL', 'PAPER', 'PARIS', 'PARTY', 'PEACE', 'PETER', 'PHASE', 'PHONE', 'PHOTO', 'PIANO', 'PIECE', 'PILOT', 'PITCH', 'PLACE', 'PLAIN', 'PLANE', 'PLANT', 'PLATE', 'POINT', 'POUND', 'POWER', 'PRESS', 'PRICE', 'PRIDE', 'PRIME', 'PRINT', 'PRIOR', 'PRIZE', 'PROOF', 'PROUD', 'PROVE', 'QUEEN', 'QUICK', 'QUIET', 'QUITE', 'RADIO', 'RAISE', 'RANGE', 'RAPID', 'RATIO', 'REACH', 'READY', 'REALM', 'REBEL', 'REFER', 'RELAX', 'REPLY', 'RIGHT', 'RIGID', 'RIVER', 'ROBOT', 'ROCKY', 'ROGER', 'ROMAN', 'ROUGH', 'ROUND', 'ROUTE', 'ROYAL', 'RURAL', 'SALLY', 'SCALE', 'SCARE', 'SCENE', 'SCOPE', 'SCORE', 'SENSE', 'SERVE', 'SEVEN', 'SHALL', 'SHAPE', 'SHARE', 'SHARP', 'SHEET', 'SHELF', 'SHELL', 'SHIFT', 'SHINE', 'SHIRT', 'SHOCK', 'SHOOT', 'SHORT', 'SHOWN', 'SIGHT', 'SILLY', 'SINCE', 'SIXTH', 'SIXTY', 'SIZED', 'SKILL', 'SLEEP', 'SLIDE', 'SMALL', 'SMART', 'SMILE', 'SMITH', 'SMOKE', 'SNAKE', 'SNOW', 'SOLID', 'SOLVE', 'SORRY', 'SOUND', 'SOUTH', 'SPACE', 'SPARE', 'SPEAK', 'SPEED', 'SPEND', 'SPENT', 'SPLIT', 'SPOKE', 'SPORT', 'STAFF', 'STAGE', 'STAKE', 'STAND', 'START', 'STATE', 'STEAM', 'STEEL', 'STEEP', 'STEER', 'STICK', 'STILL', 'STOCK', 'STONE', 'STOOD', 'STORE', 'STORM', 'STORY', 'STRIP', 'STUCK', 'STUDY', 'STUFF', 'STYLE', 'SUGAR', 'SUITE', 'SUPER', 'SWEET', 'SWORD', 'TABLE', 'TAKEN', 'TASTE', 'TAXES', 'TEACH', 'TERRY', 'TEXAS', 'THANK', 'THEFT', 'THEIR', 'THEME', 'THERE', 'THESE', 'THICK', 'THING', 'THINK', 'THIRD', 'THOSE', 'THREE', 'THREW', 'THROW', 'THUMB', 'TIGHT', 'TIRED', 'TITLE', 'TODAY', 'TOPIC', 'TOTAL', 'TOUCH', 'TOUGH', 'TOWER', 'TRACK', 'TRADE', 'TRAIN', 'TREAT', 'TREND', 'TRIAL', 'TRIBE', 'TRICK', 'TRIED', 'TRIES', 'TRUCK', 'TRULY', 'TRUST', 'TRUTH', 'TWICE', 'UNCLE', 'UNDER', 'UNDUE', 'UNION', 'UNITY', 'UNTIL', 'UPPER', 'UPSET', 'URBAN', 'USAGE', 'USUAL', 'VALID', 'VALUE', 'VIDEO', 'VIRUS', 'VISIT', 'VITAL', 'VOCAL', 'VOICE', 'WASTE', 'WATCH', 'WATER', 'WHEEL', 'WHERE', 'WHICH', 'WHILE', 'WHITE', 'WHOLE', 'WHOSE', 'WOMAN', 'WOMEN', 'WORLD', 'WORRY', 'WORSE', 'WORST', 'WORTH', 'WOULD', 'WRITE', 'WRONG', 'WROTE', 'YOUNG', 'YOUTH'],
    4: ['ABLE', 'ACID', 'AGED', 'ALSO', 'AREA', 'ARMY', 'BACK', 'BALL', 'BAND', 'BANK', 'BASE', 'BEAT', 'BEEN', 'BELL', 'BEST', 'BILL', 'BIRD', 'BLOW', 'BLUE', 'BOAT', 'BODY', 'BONE', 'BOOK', 'BORN', 'BOTH', 'BOYS', 'CAME', 'CAMP', 'CARD', 'CARE', 'CASE', 'CASH', 'CAST', 'CELL', 'CHAT', 'CITY', 'CLUB', 'COAL', 'COAT', 'CODE', 'COLD', 'COME', 'COOL', 'COPY', 'CORN', 'COST', 'CREW', 'CROP', 'DARK', 'DATA', 'DATE', 'DAYS', 'DEAD', 'DEAL', 'DEAR', 'DECK', 'DEEP', 'DESK', 'DIED', 'DOES', 'DONE', 'DOOR', 'DOWN', 'DRAW', 'DREW', 'DROP', 'DRUG', 'DUAL', 'EACH', 'EARL', 'EAST', 'EASY', 'EDGE', 'ELSE', 'EVEN', 'EVER', 'EVIL', 'FACE', 'FACT', 'FAIL', 'FAIR', 'FALL', 'FARM', 'FAST', 'FEAR', 'FEED', 'FEEL', 'FEET', 'FELL', 'FELT', 'FILE', 'FILL', 'FILM', 'FIND', 'FINE', 'FIRE', 'FIRM', 'FISH', 'FIVE', 'FLAT', 'FLEW', 'FLOW', 'FOLK', 'FOOD', 'FOOT', 'FORD', 'FORM', 'FORT', 'FOUR', 'FREE', 'FROM', 'FUEL', 'FULL', 'FUND', 'GAIN', 'GAME', 'GATE', 'GAVE', 'GEAR', 'GIRL', 'GIVE', 'GLAD', 'GOAL', 'GOES', 'GOLD', 'GONE', 'GOOD', 'GRAB', 'GRAY', 'GREW', 'GRID', 'GROW', 'GULF', 'GUYS', 'HACK', 'HAIR', 'HALF', 'HALL', 'HAND', 'HANG', 'HARD', 'HARM', 'HATE', 'HAVE', 'HEAD', 'HEAR', 'HEAT', 'HELD', 'HELL', 'HELP', 'HERE', 'HERO', 'HIDE', 'HIGH', 'HILL', 'HINT', 'HIRE', 'HOLD', 'HOLE', 'HOLY', 'HOME', 'HOPE', 'HOST', 'HOUR', 'HUGE', 'HUNG', 'HUNT', 'HURT', 'IDEA', 'INCH', 'INTO', 'IRON', 'ITEM', 'JACK', 'JANE', 'JEAN', 'JOHN', 'JOIN', 'JUMP', 'JUNE', 'JURY', 'JUST', 'KEEN', 'KEEP', 'KENT', 'KEPT', 'KILL', 'KIND', 'KING', 'KNEW', 'KNOW', 'LACK', 'LADY', 'LAID', 'LAKE', 'LAND', 'LANE', 'LAST', 'LATE', 'LEAD', 'LEAF', 'LEAN', 'LEFT', 'LESS', 'LIED', 'LIFE', 'LIFT', 'LIKE', 'LINE', 'LINK', 'LIST', 'LIVE', 'LOAN', 'LOCK', 'LONG', 'LOOK', 'LORD', 'LOSE', 'LOSS', 'LOST', 'LOTS', 'LOUD', 'LOVE', 'LUCK', 'MADE', 'MAIL', 'MAIN', 'MAKE', 'MALE', 'MANY', 'MARK', 'MASS', 'MATH', 'MEAL', 'MEAN', 'MEAT', 'MEET', 'MIND', 'MINE', 'MISS', 'MODE', 'MORE', 'MOST', 'MOVE', 'MUCH', 'MUST', 'NAME', 'NAVY', 'NEAR', 'NECK', 'NEED', 'NEWS', 'NEXT', 'NICE', 'NINE', 'NODE', 'NONE', 'NOON', 'NOSE', 'NOTE', 'OKAY', 'ONCE', 'ONLY', 'ONTO', 'OPEN', 'OVER', 'PACE', 'PACK', 'PAGE', 'PAID', 'PAIN', 'PAIR', 'PALE', 'PARK', 'PART', 'PASS', 'PAST', 'PATH', 'PEAK', 'PICK', 'PILE', 'PINK', 'PLAN', 'PLAY', 'PLOT', 'PLUS', 'POEM', 'POET', 'POLE', 'POLL', 'POOL', 'POOR', 'PORT', 'POST', 'POUR', 'PULL', 'PUSH', 'QUIT', 'RACE', 'RAIL', 'RAIN', 'RANK', 'RARE', 'RATE', 'READ', 'REAL', 'REAR', 'RELY', 'RENT', 'REST', 'RICE', 'RICH', 'RIDE', 'RING', 'RISE', 'RISK', 'ROAD', 'ROCK', 'ROLE', 'ROLL', 'ROOM', 'ROOT', 'ROSE', 'RULE', 'RUNS', 'RUSH', 'SAFE', 'SAID', 'SAIL', 'SAKE', 'SALE', 'SALT', 'SAME', 'SAND', 'SAVE', 'SAYS', 'SEAT', 'SEEK', 'SEEM', 'SEEN', 'SELF', 'SELL', 'SEND', 'SENT', 'SHIP', 'SHOP', 'SHOT', 'SHOW', 'SHUT', 'SICK', 'SIDE', 'SIGN', 'SING', 'SINK', 'SIZE', 'SKIN', 'SLIP', 'SLOW', 'SNAP', 'SNOW', 'SOFT', 'SOIL', 'SOLD', 'SOLE', 'SOME', 'SONG', 'SOON', 'SORT', 'SOUL', 'SPIN', 'SPOT', 'STAR', 'STAY', 'STEP', 'STOP', 'SUCH', 'SUIT', 'SURE', 'TAKE', 'TALE', 'TALK', 'TALL', 'TANK', 'TAPE', 'TASK', 'TEAM', 'TELL', 'TEND', 'TERM', 'TEST', 'TEXT', 'THAN', 'THAT', 'THEM', 'THEN', 'THEY', 'THIN', 'THIS', 'THUS', 'TIDE', 'TIED', 'TIME', 'TINY', 'TOLD', 'TONE', 'TOOK', 'TOOL', 'TOPS', 'TORN', 'TOWN', 'TREE', 'TRIP', 'TRUE', 'TUNE', 'TURN', 'TYPE', 'UNIT', 'UPON', 'USED', 'USER', 'VARY', 'VAST', 'VERY', 'VIEW', 'VOTE', 'WAGE', 'WAIT', 'WAKE', 'WALK', 'WALL', 'WANT', 'WARD', 'WARM', 'WASH', 'WAVE', 'WAYS', 'WEAK', 'WEAR', 'WEEK', 'WELL', 'WENT', 'WERE', 'WEST', 'WHAT', 'WHEN', 'WIDE', 'WIFE', 'WILD', 'WILL', 'WIND', 'WINE', 'WING', 'WIRE', 'WISE', 'WISH', 'WITH', 'WOLF', 'WOOD', 'WORD', 'WORE', 'WORK', 'WORN', 'YARD', 'YEAR', 'YOUR', 'ZERO', 'ZONE'],
    3: ['ACE', 'ACT', 'ADD', 'AGE', 'AGO', 'AID', 'AIM', 'AIR', 'ALL', 'AND', 'ANT', 'ANY', 'APE', 'ARE', 'ARK', 'ARM', 'ART', 'ASK', 'ATE', 'AWE', 'AXE', 'BAD', 'BAG', 'BAN', 'BAR', 'BAT', 'BAY', 'BED', 'BEE', 'BET', 'BIG', 'BIN', 'BIT', 'BOW', 'BOX', 'BOY', 'BUD', 'BUG', 'BUN', 'BUS', 'BUT', 'BUY', 'CAB', 'CAN', 'CAP', 'CAR', 'CAT', 'COB', 'COD', 'COW', 'CRY', 'CUB', 'CUD', 'CUP', 'CUT', 'DAD', 'DAM', 'DAY', 'DEN', 'DEW', 'DID', 'DIE', 'DIG', 'DIM', 'DIP', 'DOC', 'DOG', 'DOT', 'DRY', 'DUB', 'DUD', 'DUE', 'DUG', 'DUN', 'DYE', 'EAR', 'EAT', 'EEL', 'EGG', 'ELF', 'ELK', 'ELM', 'END', 'ERA', 'EVE', 'EWE', 'EYE', 'FAD', 'FAN', 'FAR', 'FAT', 'FAX', 'FED', 'FEE', 'FEW', 'FIG', 'FIN', 'FIR', 'FIT', 'FIX', 'FLY', 'FOE', 'FOG', 'FOR', 'FOX', 'FRY', 'FUN', 'FUR', 'GAB', 'GAG', 'GAL', 'GAP', 'GAS', 'GAY', 'GEL', 'GEM', 'GET', 'GIG', 'GIN', 'GOB', 'GOD', 'GOO', 'GOT', 'GUM', 'GUN', 'GUT', 'GUY', 'GYM', 'HAD', 'HAG', 'HAM', 'HAS', 'HAT', 'HAY', 'HEN', 'HER', 'HEX', 'HEY', 'HID', 'HIM', 'HIP', 'HIS', 'HIT', 'HOG', 'HOP', 'HOT', 'HOW', 'HUB', 'HUE', 'HUG', 'HUM', 'HUN', 'HUT', 'ICE', 'ILL', 'IMP', 'INK', 'INN', 'ION', 'IRE', 'IRK', 'ITS', 'IVY', 'JAB', 'JAG', 'JAM', 'JAR', 'JAW', 'JAY', 'JET', 'JIG', 'JOB', 'JOG', 'JOT', 'JOY', 'JUG', 'JUT', 'KEG', 'KEY', 'KID', 'KIN', 'KIT', 'LAB', 'LAD', 'LAG', 'LAP', 'LAW', 'LAX', 'LAY', 'LEA', 'LED', 'LEG', 'LET', 'LID', 'LIE', 'LIP', 'LIT', 'LOG', 'LOT', 'LOW', 'LYE', 'MAC', 'MAD', 'MAM', 'MAN', 'MAP', 'MAR', 'MAT', 'MAW', 'MAY', 'MEN', 'MET', 'MID', 'MIX', 'MOB', 'MOD', 'MOM', 'MOP', 'MOW', 'MUD', 'MUG', 'NAB', 'NAG', 'NAP', 'NAY', 'NET', 'NEW', 'NIT', 'NOB', 'NOD', 'NOR', 'NOT', 'NOW', 'NUB', 'NUN', 'NUT', 'OAK', 'OAR', 'OAT', 'ODD', 'OIL', 'OLD', 'ONE', 'ORB', 'ORE', 'OUR', 'OUT', 'OWE', 'OWL', 'OWN', 'PAD', 'PAL', 'PAN', 'PAP', 'PAR', 'PAT', 'PAW', 'PAY', 'PEA', 'PEG', 'PEN', 'PEP', 'PET', 'PEW', 'PIE', 'PIG', 'PIN', 'PIT', 'PLY', 'POD', 'POP', 'POT', 'POW', 'PRO', 'PRY', 'PUB', 'PUG', 'PUN', 'PUP', 'PUS', 'PUT', 'RAG', 'RAM', 'RAN', 'RAP', 'RAT', 'RAW', 'RAY', 'RED', 'REP', 'RIB', 'RID', 'RIG', 'RIM', 'RIP', 'ROB', 'ROD', 'ROE', 'ROT', 'ROW', 'RUB', 'RUG', 'RUM', 'RUN', 'RUT', 'RYE', 'SAC', 'SAD', 'SAG', 'SAP', 'SAT', 'SAW', 'SAY', 'SEA', 'SEW', 'SHE', 'SHY', 'SIN', 'SIP', 'SIR', 'SIS', 'SIT', 'SIX', 'SKI', 'SKY', 'SLY', 'SOB', 'SOD', 'SON', 'SOP', 'SOT', 'SOW', 'SOY', 'SPA', 'SPY', 'STY', 'SUB', 'SUM', 'SUN', 'TAB', 'TAD', 'TAG', 'TAN', 'TAP', 'TAR', 'TAT', 'TAX', 'TEA', 'TEN', 'THE', 'TIC', 'TIE', 'TIN', 'TIP', 'TOE', 'TON', 'TOO', 'TOP', 'TOW', 'TOY', 'TRY', 'TUB', 'TUG', 'TUT', 'TWO', 'URN', 'USE', 'VAN', 'VAT', 'VET', 'VIA', 'VIE', 'VOW', 'WAD', 'WAG', 'WAR', 'WAS', 'WAX', 'WAY', 'WEB', 'WED', 'WET', 'WHO', 'WHY', 'WIG', 'WIN', 'WIT', 'WOE', 'WOK', 'WON', 'WOO', 'WOW', 'YAK', 'YAM', 'YAP', 'YAW', 'YEA', 'YEP', 'YES', 'YET', 'YEW', 'YIN', 'YIP', 'YON', 'YOU', 'YOW', 'YUK', 'YUM', 'ZAG', 'ZAP', 'ZED', 'ZEE', 'ZEN', 'ZIP', 'ZIT', 'ZOO', 'ABS', 'ACH', 'ADS', 'AFT', 'AHA', 'AHS', 'ALS', 'AMP', 'ANI', 'APT', 'ARC', 'ARF', 'ASH', 'AUK', 'AVE', 'AWL', 'AYE', 'BAA', 'BAH', 'BAM', 'BAS', 'BAX', 'BEL', 'BEN', 'BIB', 'BID', 'BIM', 'BIS', 'BOA', 'BOB', 'BOG', 'BOP', 'BOT', 'BOZ', 'BRA', 'BRO', 'BUB', 'BUM', 'CAD', 'CAM', 'CAW', 'CHI', 'CIG', 'COG', 'COO', 'COP', 'COT', 'COX', 'COY', 'COZ', 'CUE', 'CUR', 'DAB', 'DAN', 'DEL', 'DOE', 'DOH', 'DOS', 'DUH', 'EAT', 'EEK', 'ELK', 'ELS', 'EMU', 'ERG', 'ERR', 'ETA', 'ETH', 'EWW', 'FAG', 'FEH', 'FEZ', 'FIB', 'FID', 'FIE', 'FIG', 'FIT', 'FLU', 'FOB', 'FOH', 'FOP', 'GAD', 'GAM', 'GAR', 'GAW', 'GEE', 'GHI', 'GIG', 'GNU', 'GOA', 'GOL', 'GOX', 'GUL', 'GUS', 'HAH', 'HAJ', 'HAP', 'HAW', 'HEM', 'HEP', 'HEW', 'HIC', 'HIE', 'HIN', 'HIS', 'HOB', 'HOD', 'HOE', 'HON', 'HOP', 'HOY', 'HUH', 'HUN', 'HUP', 'HUT', 'ICH', 'ICK', 'ICY', 'IFS', 'ILK', 'INS', 'IRK', 'ISM', 'JAB', 'JAG', 'JAM', 'JAR', 'JAW', 'JAY', 'JEE', 'JET', 'JEW', 'JIG', 'JIN', 'JOB', 'JOE', 'JOG', 'JOT', 'JOW', 'JOY', 'JUG', 'JUN', 'JUS', 'JUT', 'KAB', 'KAE', 'KAS', 'KAT', 'KAY', 'KEA', 'KED', 'KEF', 'KEG', 'KEN', 'KEP', 'KET', 'KEX', 'KEY', 'KHI', 'KID', 'KIF', 'KIN', 'KIP', 'KIR', 'KIS', 'KIT', 'KOA', 'KOB', 'KOI', 'KOP', 'KOR', 'KOS', 'KUE', 'LAB', 'LAC', 'LAD', 'LAG', 'LAH', 'LAM', 'LAP', 'LAR', 'LAS', 'LAT', 'LAV', 'LAW', 'LAX', 'LAY', 'LEA', 'LED', 'LEE', 'LEG', 'LEI', 'LEK', 'LES', 'LET', 'LEU', 'LEV', 'LEW', 'LEX', 'LEY', 'LEZ', 'LIB', 'LID', 'LIE', 'LIN', 'LIP', 'LIS', 'LIT', 'LOB', 'LOG', 'LOO', 'LOP', 'LOT', 'LOW', 'LOX', 'LUG', 'LUV', 'LUX', 'LYE', 'MAC', 'MAD', 'MAE', 'MAG', 'MAN', 'MAP', 'MAR', 'MAS', 'MAT', 'MAW', 'MAX', 'MAY', 'MED', 'MEL', 'MEN', 'MET', 'MEW', 'MID', 'MIG', 'MIL', 'MIM', 'MIR', 'MIS', 'MIX', 'MOB', 'MOC', 'MOD', 'MOE', 'MOG', 'MOM', 'MON', 'MOO', 'MOP', 'MOR', 'MOS', 'MOT', 'MOW', 'MUD', 'MUG', 'MUM', 'MUN', 'MUS', 'MUT', 'MUX', 'NAB', 'NAE', 'NAG', 'NAH', 'NAM', 'NAN', 'NAP', 'NAW', 'NAY', 'NEE', 'NET', 'NEW', 'NIB', 'NIL', 'NIM', 'NIP', 'NIT', 'NIX', 'NOB', 'NOD', 'NOG', 'NOH', 'NOM', 'NOO', 'NOR', 'NOS', 'NOT', 'NOW', 'NTH', 'NUB', 'NUN', 'NUT', 'OAF', 'OAK', 'OAR', 'OAT', 'OBE', 'OBI', 'OCA', 'OCH', 'ODD', 'ODE', 'ODS', 'OES', 'OFF', 'OFT', 'OHM', 'OHO', 'OHS', 'OIK', 'OIL', 'OKA', 'OKE', 'OLD', 'OLE', 'OMS', 'ONE', 'ONO', 'ONS', 'OOF', 'OOH', 'OOT', 'OPE', 'OPS', 'OPT', 'ORA', 'ORB', 'ORC', 'ORE', 'ORS', 'ORT', 'OSE', 'OUD', 'OUR', 'OUT', 'OVA', 'OWE', 'OWL', 'OWN', 'OWT', 'OXO', 'OXY', 'OYE', 'OYS', 'PAC', 'PAD', 'PAH', 'PAL', 'PAM', 'PAN', 'PAP', 'PAR', 'PAS', 'PAT', 'PAW', 'PAX', 'PAY', 'PEA', 'PEC', 'PED', 'PEE', 'PEG', 'PEH', 'PEN', 'PEP', 'PER', 'PES', 'PET', 'PEW', 'PHI', 'PIC', 'PIE', 'PIG', 'PIN', 'PIP', 'PIS', 'PIT', 'PIU', 'PLY', 'POD', 'POH', 'POI', 'POL', 'POM', 'POP', 'POS', 'POT', 'POW', 'POX', 'POZ', 'PRO', 'PRY', 'PSI', 'PUB', 'PUD', 'PUG', 'PUH', 'PUL', 'PUN', 'PUP', 'PUR', 'PUS', 'PUT', 'PUY', 'PYA', 'PYE', 'PYX', 'QAT', 'QUA', 'RAD', 'RAG', 'RAH', 'RAI', 'RAJ', 'RAM', 'RAN', 'RAP', 'RAS', 'RAT', 'RAW', 'RAX', 'RAY', 'REB', 'REC', 'RED', 'REF', 'REG', 'REI', 'REM', 'REP', 'RES', 'RET', 'REV', 'REW', 'REX', 'RHO', 'RIA', 'RIB', 'RID', 'RIF', 'RIG', 'RIM', 'RIN', 'RIP', 'RIT', 'ROB', 'ROC', 'ROD', 'ROE', 'ROM', 'ROT', 'ROW', 'RUB', 'RUC', 'RUD', 'RUE', 'RUG', 'RUM', 'RUN', 'RUT', 'RYA', 'RYE', 'SAB', 'SAC', 'SAD', 'SAE', 'SAG', 'SAI', 'SAL', 'SAP', 'SAR', 'SAT', 'SAU', 'SAW', 'SAX', 'SAY', 'SEA', 'SEE', 'SEG', 'SEI', 'SEL', 'SEN', 'SER', 'SET', 'SEW', 'SEX', 'SHA', 'SHE', 'SHY', 'SIB', 'SIC', 'SIM', 'SIN', 'SIP', 'SIR', 'SIS', 'SIT', 'SIX', 'SKA', 'SKI', 'SKY', 'SLY', 'SOB', 'SOD', 'SOH', 'SOL', 'SOM', 'SON', 'SOP', 'SOS', 'SOT', 'SOU', 'SOV', 'SOW', 'SOX', 'SOY', 'SOZ', 'SPA', 'SPY', 'STY', 'SUB', 'SUD', 'SUE', 'SUI', 'SUK', 'SUM', 'SUN', 'SUP', 'SUR', 'SUS', 'SYN', 'TAB', 'TAC', 'TAD', 'TAE', 'TAG', 'TAH', 'TAI', 'TAJ', 'TAK', 'TAM', 'TAN', 'TAO', 'TAP', 'TAR', 'TAS', 'TAT', 'TAU', 'TAV', 'TAW', 'TAX', 'TEA', 'TED', 'TEE', 'TEF', 'TEG', 'TEL', 'TEN', 'TES', 'TET', 'TEW', 'TEX', 'THE', 'THO', 'THY', 'TIC', 'TID', 'TIE', 'TIG', 'TIK', 'TIL', 'TIN', 'TIP', 'TIS', 'TIT', 'TIX', 'TOC', 'TOD', 'TOE', 'TOG', 'TOM', 'TON', 'TOO', 'TOP', 'TOR', 'TOT', 'TOW', 'TOY', 'TRY', 'TSK', 'TUB', 'TUG', 'TUI', 'TUK', 'TUM', 'TUN', 'TUP', 'TUT', 'TUX', 'TWA', 'TWO', 'TYE', 'UDO', 'UDS', 'UGH', 'UGS', 'UKE', 'ULE', 'ULS', 'UMM', 'UMP', 'UMS', 'UNS', 'UPO', 'UPS', 'URB', 'URD', 'URN', 'URP', 'USE', 'UTA', 'UTE', 'UTS', 'VAC', 'VAN', 'VAR', 'VAS', 'VAT', 'VAU', 'VAV', 'VAW', 'VEE', 'VET', 'VEX', 'VIA', 'VID', 'VIE', 'VIG', 'VIM', 'VIS', 'VOE', 'VOW', 'VOX', 'VUG', 'VUM', 'WAB', 'WAD', 'WAE', 'WAG', 'WAN', 'WAP', 'WAR', 'WAS', 'WAT', 'WAW', 'WAX', 'WAY', 'WEB', 'WED', 'WEE', 'WEN', 'WET', 'WEX', 'WEY', 'WHA', 'WHO', 'WHY', 'WIG', 'WIN', 'WIS', 'WIT', 'WIZ', 'WOE', 'WOG', 'WOK', 'WON', 'WOO', 'WOP', 'WOS', 'WOT', 'WOW', 'WRY', 'WUD', 'WYE', 'WYN', 'XIS', 'YAG', 'YAH', 'YAK', 'YAM', 'YAP', 'YAR', 'YAS', 'YAW', 'YAY', 'YEA', 'YEH', 'YEN', 'YEP', 'YER', 'YES', 'YET', 'YEW', 'YEX', 'YID', 'YIN', 'YIP', 'YOB', 'YOD', 'YOK', 'YOM', 'YON', 'YOU', 'YOW', 'YUG', 'YUK', 'YUM', 'YUP', 'YUS', 'ZAG', 'ZAP', 'ZAR', 'ZAS', 'ZAX', 'ZEA', 'ZED', 'ZEE', 'ZEK', 'ZEN', 'ZEP', 'ZES', 'ZET', 'ZEX', 'ZHO', 'ZIG', 'ZIN', 'ZIP', 'ZIS', 'ZIT', 'ZIZ', 'ZOA', 'ZOD', 'ZOL', 'ZOO', 'ZOS', 'ZUZ', 'ZYM'],
    2: ['AM', 'AN', 'AS', 'AT', 'AX', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN', 'IS', 'IT', 'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'OX', 'SO', 'TO', 'UP', 'US', 'WE', 'AD', 'AH', 'HI', 'HM', 'HO', 'LO', 'MA', 'OH', 'OW', 'PA', 'RE', 'SH', 'UM', 'YO', 'AY', 'BA', 'EH', 'FA', 'LA', 'MM', 'MO', 'OP', 'OO', 'ST', 'UH', 'UN', 'YE', 'ZE', 'AG', 'AL', 'AR', 'AW', 'BO', 'ED', 'EF', 'EL', 'EM', 'EN', 'ER', 'ET', 'EX', 'GI', 'GU', 'ID', 'JA', 'JO', 'KA', 'KI', 'LI']', 'SAT', 'SAW', 'SAY', 'SEA', 'SEW', 'SHE', 'SHY', 'SIN', 'SIP', 'SIR', 'SIS', 'SIT', 'SIX', 'SKI', 'SKY', 'SLY', 'SOB', 'SOD', 'SON', 'SOP', 'SOT', 'SOW', 'SOY', 'SPA', 'SPY', 'STY', 'SUB', 'SUM', 'SUN', 'TAB', 'TAD', 'TAG', 'TAN', 'TAP', 'TAR', 'TAT', 'TAX', 'TEA', 'TEN', 'THE', 'TIC', 'TIE', 'TIN', 'TIP', 'TOE', 'TON', 'TOO', 'TOP', 'TOW', 'TOY', 'TRY', 'TUB', 'TUG', 'TUT', 'TWO', 'URN', 'USE', 'VAN', 'VAT', 'VET', 'VIA', 'VIE', 'VOW', 'WAD', 'WAG', 'WAR', 'WAS', 'WAX', 'WAY', 'WEB', 'WED', 'WET', 'WHO', 'WHY', 'WIG', 'WIN', 'WIT', 'WOE', 'WOK', 'WON', 'WOO', 'WOW', 'YAK', 'YAM', 'YAP', 'YAW', 'YEA', 'YEP', 'YES', 'YET', 'YEW', 'YIN', 'YIP', 'YON', 'YOU', 'YOW', 'YUK', 'YUM', 'ZAG', 'ZAP', 'ZED', 'ZEE', 'ZEN', 'ZIP', 'ZIT', 'ZOO'],
    2: ['AM', 'AN', 'AS', 'AT', 'AX', 'BE', 'BY', 'DO', 'GO', 'HE', 'IF', 'IN', 'IS', 'IT', 'ME', 'MY', 'NO', 'OF', 'ON', 'OR', 'OX', 'SO', 'TO', 'UP', 'US', 'WE']
};

// Game initialization
window.addEventListener('load', function() {
    console.log('Page loaded, trying to show modal');
    const modal = document.getElementById('modal');
    console.log('Modal element:', modal);
    if (modal) {
        showModal();
        console.log('Modal should be visible now');
    } else {
        console.error('Modal element not found!');
    }
    updateCoinFlip();
});

// Modal functions
function showModal() {
    document.getElementById('modal').style.display = 'flex';
}

function hideModal() {
    document.getElementById('modal').style.display = 'none';
}

// Coin flip logic
function updateCoinFlip() {
    const isHeads = Math.random() < 0.5;
    const coinFlip1 = document.getElementById('coinFlip1');
    const coinFlip2 = document.getElementById('coinFlip2');
    
    coinFlip1.textContent = isHeads ? "IF HEADS YOU'RE FIRST" : "IF TAILS YOU'RE FIRST";
    coinFlip2.textContent = isHeads ? "IF TAILS YOU'RE FIRST" : "IF HEADS YOU'RE FIRST";
    
    return isHeads;
}

// Main game setup function
function startGame() {
    const player1Name = getPlayerName('player1Name');
    const player2Name = getPlayerName('player2Name');
    const autoGenerate = document.getElementById('autoGen').checked;
    
    updateFleetTitles(player1Name, player2Name);
    
    if (autoGenerate) {
        generateAllWords();
    }
    
    hideModal();
    
    // Print after a brief delay to ensure all updates are applied
    setTimeout(() => {
        window.print();
    }, 100);
}

// Make startGame available globally for onclick
window.startGame = startGame;

// Helper functions
function getPlayerName(inputId) {
    return document.getElementById(inputId).value.trim();
}

function updateFleetTitles(player1Name, player2Name) {
    // Update titles - each player sees the other as their opponent
    if (player1Name) {
        document.getElementById('your-title1').textContent = player1Name;
        document.getElementById('opponent-title2').textContent = player1Name;
    }
    
    if (player2Name) {
        document.getElementById('your-title2').textContent = player2Name;
        document.getElementById('opponent-title1').textContent = player2Name;
    }
}

// Word generation functions
function generateAllWords() {
    generatePlayerWords('p1');
    generatePlayerWords('p2');
}

function generatePlayerWords(player) {
    const usedWords = new Set();
    
    const getUniqueWord = (length) => {
        let attempts = 0;
        let word;
        
        do {
            word = getRandomWord(length);
            attempts++;
        } while (usedWords.has(word) && attempts < 20);
        
        usedWords.add(word);
        return word;
    };
    
    // Generate words for each ship type
    fillWord(`your-5-${player}`, getUniqueWord(5));
    fillWord(`your-4-${player}`, getUniqueWord(4));
    
    // Generate two different 3-letter words
    const word3a = getUniqueWord(3);
    fillWord(`your-3a-${player}`, word3a);
    
    let word3b;
    do {
        word3b = getUniqueWord(3);
    } while (word3b === word3a);
    fillWord(`your-3b-${player}`, word3b);
    
    fillWord(`your-2-${player}`, getUniqueWord(2));
}

function getRandomWord(length) {
    const wordList = WORD_LISTS[length];
    const randomIndex = Math.floor(Math.random() * wordList.length);
    return wordList[randomIndex];
}

function fillWord(containerId, word) {
    const container = document.getElementById(containerId);
    
    if (!container) {
        console.warn(`Container with ID '${containerId}' not found`);
        return;
    }
    
    const boxes = container.children;
    
    for (let i = 0; i < word.length && i < boxes.length; i++) {
        boxes[i].textContent = word[i];
    }
}