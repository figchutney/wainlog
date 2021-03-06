import dataclasses
import datetime
import enum


@enum.unique
class Book(enum.Enum):
    EASTERN = "EASTERN"
    FAR_EASTERN = "FAR_EASTERN"
    CENTRAL = "CENTRAL"
    SOUTHERN = "SOUTHERN"
    NORTHERN = "NORTHERN"
    NORTH_WESTERN = "NORTH_WESTERN"
    WESTERN = "WESTERN"


@enum.unique
class FellName(enum.Enum):
    ALLEN_CRAGS = "ALLEN_CRAGS"
    ANGLETARN_PIKES = "ANGLETARN_PIKES"
    ARD_CRAGS = "ARD_CRAGS"
    ARMBOTH_FELL = "ARMBOTH_FELL"
    ARNISON_CRAG = "ARNISON_CRAG"
    ARTHURS_PIKE = "ARTHURS_PIKE"
    BAKESTALL = "BAKESTALL"
    BANNERDALE_CRAGS = "BANNERDALE_CRAGS"
    BARF = "BARF"
    BARROW = "BARROW"
    BASE_BROWN = "BASE_BROWN"
    BEDA_FELL = "BEDA_FELL"
    BINSEY = "BINSEY"
    BIRKHOUSE_MOOR = "BIRKHOUSE_MOOR"
    BIRKS = "BIRKS"
    BLACK_FELL = "BLACK_FELL"
    BLAKE_FELL = "BLAKE_FELL"
    BLEA_RIGG = "BLEA_RIGG"
    BLEABERRY_FELL = "BLEABERRY_FELL"
    BLENCATHRA = "BLENCATHRA"
    BONSCALE_PIKE = "BONSCALE_PIKE"
    BOWFELL = "BOWFELL"
    BOWSCALE_FELL = "BOWSCALE_FELL"
    BRAE_FELL = "BRAE_FELL"
    BRANDRETH = "BRANDRETH"
    BRANSTREE = "BRANSTREE"
    BRIM_FELL = "BRIM_FELL"
    BROCK_CRAGS = "BROCK_CRAGS"
    BROOM_FELL = "BROOM_FELL"
    BUCKBARROW = "BUCKBARROW"
    BURNBANK_FELL = "BURNBANK_FELL"
    CALF_CRAG = "CALF_CRAG"
    CARL_SIDE = "CARL_SIDE"
    CARROCK_FELL = "CARROCK_FELL"
    CASTLE_CRAG = "CASTLE_CRAG"
    CATBELLS = "CATBELLS"
    CATSTYE_CAM = "CATSTYE_CAM"
    CAUSEY_PIKE = "CAUSEY_PIKE"
    CAW_FELL = "CAW_FELL"
    CLOUGH_HEAD = "CLOUGH_HEAD"
    COLD_PIKE = "COLD_PIKE"
    CONISTON_OLD_MAN = "CONISTON_OLD_MAN"
    CRAG_FELL = "CRAG_FELL"
    CRINKLE_CRAGS = "CRINKLE_CRAGS"
    DALE_HEAD = "DALE_HEAD"
    DODD = "DODD"
    DOLLYWAGGON_PIKE = "DOLLYWAGGON_PIKE"
    DOVE_CRAG = "DOVE_CRAG"
    DOW_CRAG = "DOW_CRAG"
    EAGLE_CRAG = "EAGLE_CRAG"
    EEL_CRAG = "EEL_CRAG"
    ESK_PIKE = "ESK_PIKE"
    FAIRFIELD = "FAIRFIELD"
    FELLBARROW = "FELLBARROW"
    FLEETWITH_PIKE = "FLEETWITH_PIKE"
    FROSWICK = "FROSWICK"
    GAVEL_FELL = "GAVEL_FELL"
    GIBSON_KNOTT = "GIBSON_KNOTT"
    GLARAMARA = "GLARAMARA"
    GLENRIDDING_DODD = "GLENRIDDING_DODD"
    GOWBARROW_FELL = "GOWBARROW_FELL"
    GRANGE_FELL = "GRANGE_FELL"
    GRASMOOR = "GRASMOOR"
    GRAY_CRAG = "GRAY_CRAG"
    GRAYSTONES = "GRAYSTONES"
    GREAT_BORNE = "GREAT_BORNE"
    GREAT_CALVA = "GREAT_CALVA"
    GREAT_CARRS = "GREAT_CARRS"
    GREAT_COCKUP = "GREAT_COCKUP"
    GREAT_CRAG = "GREAT_CRAG"
    GREAT_DODD = "GREAT_DODD"
    GREAT_END = "GREAT_END"
    GREAT_GABLE = "GREAT_GABLE"
    GREAT_MELL_FELL = "GREAT_MELL_FELL"
    GREAT_RIGG = "GREAT_RIGG"
    GREAT_SCA_FELL = "GREAT_SCA_FELL"
    GREEN_CRAG = "GREEN_CRAG"
    GREEN_GABLE = "GREEN_GABLE"
    GREY_CRAG = "GREY_CRAG"
    GREY_FRIAR = "GREY_FRIAR"
    GREY_KNOTTS = "GREY_KNOTTS"
    GRIKE = "GRIKE"
    GRISEDALE_PIKE = "GRISEDALE_PIKE"
    HALLIN_FELL = "HALLIN_FELL"
    HARD_KNOTT = "HARD_KNOTT"
    HARRISON_STICKLE = "HARRISON_STICKLE"
    HART_CRAG = "HART_CRAG"
    HART_SIDE = "HART_SIDE"
    HARTER_FELL_ESKDALE = "HARTER_FELL_ESKDALE"
    HARTER_FELL_MARDALE = "HARTER_FELL_MARDALE"
    HARTSOP_ABOVE_HOW = "HARTSOP_ABOVE_HOW"
    HARTSOP_DODD = "HARTSOP_DODD"
    HAYCOCK = "HAYCOCK"
    HAYSTACKS = "HAYSTACKS"
    HELM_CRAG = "HELM_CRAG"
    HELVELLYN = "HELVELLYN"
    HEN_COMB = "HEN_COMB"
    HERON_PIKE = "HERON_PIKE"
    HIGH_CRAG = "HIGH_CRAG"
    HIGH_HARTSOP_DODD = "HIGH_HARTSOP_DODD"
    HIGH_PIKE_CALDBECK = "HIGH_PIKE_CALDBECK"
    HIGH_PIKE_SCANDALE = "HIGH_PIKE_SCANDALE"
    HIGH_RAISE_HIGH_STREET = "HIGH_RAISE_HIGH_STREET"
    HIGH_RAISE_LANGDALE = "HIGH_RAISE_LANGDALE"
    HIGH_RIGG = "HIGH_RIGG"
    HIGH_SEAT = "HIGH_SEAT"
    HIGH_SPY = "HIGH_SPY"
    HIGH_STILE = "HIGH_STILE"
    HIGH_STREET = "HIGH_STREET"
    HIGH_TOVE = "HIGH_TOVE"
    HINDSCARTH = "HINDSCARTH"
    HOLME_FELL = "HOLME_FELL"
    HOPEGILL_HEAD = "HOPEGILL_HEAD"
    ILL_BELL = "ILL_BELL"
    ILLGILL_HEAD = "ILLGILL_HEAD"
    KENTMERE_PIKE = "KENTMERE_PIKE"
    KIDSTY_PIKE = "KIDSTY_PIKE"
    KIRK_FELL = "KIRK_FELL"
    KNOTT = "KNOTT"
    KNOTT_RIGG = "KNOTT_RIGG"
    LANK_RIGG = "LANK_RIGG"
    LATRIGG = "LATRIGG"
    LING_FELL = "LING_FELL"
    LINGMELL = "LINGMELL"
    LINGMOOR_FELL = "LINGMOOR_FELL"
    LITTLE_HART_CRAG = "LITTLE_HART_CRAG"
    LITTLE_MELL_FELL = "LITTLE_MELL_FELL"
    LOADPOT_HILL = "LOADPOT_HILL"
    LOFT_CRAG = "LOFT_CRAG"
    LONG_SIDE = "LONG_SIDE"
    LONGLANDS_FELL = "LONGLANDS_FELL"
    LONSCALE_FELL = "LONSCALE_FELL"
    LORDS_SEAT = "LORDS_SEAT"
    LOUGHRIGG_FELL = "LOUGHRIGG_FELL"
    LOW_FELL = "LOW_FELL"
    LOW_PIKE = "LOW_PIKE"
    MAIDEN_MOOR = "MAIDEN_MOOR"
    MARDALE_ILL_BELL = "MARDALE_ILL_BELL"
    MEAL_FELL = "MEAL_FELL"
    MELLBREAK = "MELLBREAK"
    MIDDLE_DODD = "MIDDLE_DODD"
    MIDDLE_FELL = "MIDDLE_FELL"
    MUNGRISDALE_COMMON = "MUNGRISDALE_COMMON"
    NAB_SCAR = "NAB_SCAR"
    NETHERMOST_PIKE = "NETHERMOST_PIKE"
    OUTERSIDE = "OUTERSIDE"
    PAVEY_ARK = "PAVEY_ARK"
    PIKE_OF_BLISCO = "PIKE_OF_BLISCO"
    PIKE_OF_STICKLE = "PIKE_OF_STICKLE"
    PILLAR = "PILLAR"
    PLACE_FELL = "PLACE_FELL"
    RAISE = "RAISE"
    RAMPSGILL_HEAD = "RAMPSGILL_HEAD"
    RANNERDALE_KNOTTS = "RANNERDALE_KNOTTS"
    RAVEN_CRAG = "RAVEN_CRAG"
    RED_PIKE_BUTTERMERE = "RED_PIKE_BUTTERMERE"
    RED_PIKE_WASDALE = "RED_PIKE_WASDALE"
    RED_SCREES = "RED_SCREES"
    REST_DODD = "REST_DODD"
    ROBINSON = "ROBINSON"
    ROSSETT_PIKE = "ROSSETT_PIKE"
    ROSTHWAITE_FELL = "ROSTHWAITE_FELL"
    SAIL = "SAIL"
    SALE_FELL = "SALE_FELL"
    SALLOWS = "SALLOWS"
    SCAFELL = "SCAFELL"
    SCAFELL_PIKE = "SCAFELL_PIKE"
    SCAR_CRAGS = "SCAR_CRAGS"
    SCOAT_FELL = "SCOAT_FELL"
    SEAT_SANDAL = "SEAT_SANDAL"
    SEATALLAN = "SEATALLAN"
    SEATHWAITE_FELL = "SEATHWAITE_FELL"
    SELSIDE_PIKE = "SELSIDE_PIKE"
    SERGEANT_MAN = "SERGEANT_MAN"
    SERGEANTS_CRAG = "SERGEANTS_CRAG"
    SHEFFIELD_PIKE = "SHEFFIELD_PIKE"
    SHIPMAN_KNOTTS = "SHIPMAN_KNOTTS"
    SILVER_HOW = "SILVER_HOW"
    SKIDDAW = "SKIDDAW"
    SKIDDAW_LITTLE_MAN = "SKIDDAW_LITTLE_MAN"
    SLIGHT_SIDE = "SLIGHT_SIDE"
    SOUR_HOWES = "SOUR_HOWES"
    SOUTHER_FELL = "SOUTHER_FELL"
    ST_SUNDAY_CRAG = "ST_SUNDAY_CRAG"
    STARLING_DODD = "STARLING_DODD"
    STEEL_FELL = "STEEL_FELL"
    STEEL_KNOTTS = "STEEL_KNOTTS"
    STEEPLE = "STEEPLE"
    STONE_ARTHUR = "STONE_ARTHUR"
    CAUDALE_MOOR = "CAUDALE_MOOR"
    STYBARROW_DODD = "STYBARROW_DODD"
    SWIRL_HOW = "SWIRL_HOW"
    TARN_CRAG_EASEDALE = "TARN_CRAG_EASEDALE"
    TARN_CRAG_SLEDDALE = "TARN_CRAG_SLEDDALE"
    THE_KNOTT = "THE_KNOTT"
    THE_NAB = "THE_NAB"
    THORNTHWAITE_CRAG = "THORNTHWAITE_CRAG"
    THUNACAR_KNOTT = "THUNACAR_KNOTT"
    TROUTBECK_TONGUE = "TROUTBECK_TONGUE"
    ULLOCK_PIKE = "ULLOCK_PIKE"
    ULLSCARF = "ULLSCARF"
    WALLA_CRAG = "WALLA_CRAG"
    WANDOPE = "WANDOPE"
    WANSFELL = "WANSFELL"
    WATSONS_DODD = "WATSONS_DODD"
    WETHER_HILL = "WETHER_HILL"
    WETHERLAM = "WETHERLAM"
    WHIN_RIGG = "WHIN_RIGG"
    WHINLATTER = "WHINLATTER"
    WHITE_SIDE = "WHITE_SIDE"
    WHITELESS_PIKE = "WHITELESS_PIKE"
    WHITESIDE = "WHITESIDE"
    YEWBARROW = "YEWBARROW"
    YOKE = "YOKE"


@dataclasses.dataclass
class User:
    username: str
    email: str


@dataclasses.dataclass
class Fell:
    name: FellName
    display: str
    height_rank: int
    height_m: int
    height_f: int
    os_grid_reference: str
    book: Book
    rank_in_book: int


@dataclasses.dataclass
class SummitEvent:
    username: str
    fell_name: FellName
    summit_date: datetime.datetime
