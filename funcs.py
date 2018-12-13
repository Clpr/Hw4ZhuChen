import collections  # collection operation
import codecs  # improved I/O
import random  # for sampling



# a sample text to do word segmentation
TestText = 'From: etxonss@ufsa.ericsson.se (Staffan Axelsson) Subject: NHL Swedes: Stats, April     Scoring stats for the Swedish NHL players, April :  ===================================================   Mats Sundin watch:     Most points during a season:         Kent Nilsson, Calgary Flames       -  (+)       Mats Naslund, Montreal Canadiens   -  (+)   *   Mats Sundin, Quebec Nordiques      -  (+)       Hakan Loob, Calgary Flames         -  (+)       Kent Nilsson, Calgary Flames       -  (+)        Kent Nilsson, Calgary Flames       -  (+)     Most goals during a season:         Hakan Loob, Calgary Flames         -        Kent Nilsson, Calgary Flames       -        Kent Nilsson, Calgary Flames       -        Tomas Sandstrom, LA Kings          -        Mats Naslund, Montreal Canadiens   -   *    Mats Sundin, Quebec Nordiques      -     Most assists during a season:         Kent Nilsson, Calgary Flames       -        Mats Naslund, Montreal Canadiens   -        Borje Salming, Toronto Maple Leafs -   *    Mats Sundin, Quebec Nordiques      -        Kent Nilsson, Calgary Flames       -        Borje Salming, Toronto Maple Leafs -        Thomas Steen, Winnipeg Jets        -   Ulf Samuelsson watch:     Most penalty minutes during a season:    *    Ulf Samuelsson, Pittsburgh Penguins   -   (through /)        Ulf Samuelsson, Pittsburgh Penguins   -        Ulf Samuelsson, Pittsburgh Penguins   -        Kjell Samuelsson, Philadelphia Flyers -        Ulf Samuelsson, Hartford Whalers      -        Ulf Samuelsson, Hartford Whalers      -        Borje Salming, Toronto Maple Leafs    -   -------------------------------------------------------------------------------  RL Rk Name             Team J# Ps Ht   Wt  Born      G  A  Pts  PL  Comment -- -- ---------------- ---- -- -- ---  --- --------  -- -- ---  --  -------      Mats Sundin       QUE  C  -    //               Ulf Dahlen        MIN  RW -    //                  Thomas Steen      WIN  C  -   / /              Johan Garpenlov   SJS  LW -   //               Fredrik Olausson  WIN   D  -   / /              Tomas Sandstrom   LAK   LW -    / /              Per-Erik Eklund   PHI   LW -   //            Injured      Calle Johansson   WAS   D  -   //               Nicklas Lidstrom  DET   D  -    //               Tommy Sjodin      MIN  D  -   //                Ulf Samuelsson    PIT   D  -    // Mikael Andersson  TBL  LW -   //              Michael Nylander  HFD  LW -  / /               Roger Johansson   CGY  D  -    / /              Jan Erixon        NYR  LW -    / /                 Peter Andersson   NYR  D  -    // Kjell Samuelsson  PIT  D  -   //                 Tommy Albelin     NJD   D  -    //                   Per Djoos         NYR  D  -   //              Binghampton?     Niclas Andersson  QUE  LW -    //              Halifax     Thomas Forslund   CGY  LW -   //              Salt Lake     Patrik Carnback   MON  LW -    / /              Injured     Patrik Kjellberg  MON  LW -    //              Fredericton  ------------------------------------------------------------------------------- RL=Rank Last week, Rk=Rank, J#=Jersey Number, Ps=Position, Born (mm/dd/yy) G=Goals, A=Assists, Pts=Points, PL=Points scored since Last posted list ===============================================================================   Goalie stats:   Name             Team J# Ps Ht   Wt  Born       ---------------- ---- -- -- ---  --- --------  Tommy Soderstrom  PHI  G  -    //                                         / - - - - -  T  O  T  A  L  - - - - - \\   mm/dd   vs   res  r  w/l/t  sh - sv   GP   MP  GA  GAA    SOG   SV  SV%   SO A  -----  ---- ----  -  -----  --   --   --   --  --  ---    ---  ---  ---   -- --  /   PIT  -  L  --   -             .         .  /   CHI  -  W  --   - .         .  /  @TBL  -  L  --   -           .         .  /   PIT  -  L  --   -           .        .  /  @WAS  -  T  --   -           .       .  /  @LAK -  W  --   -           .       .  /  @SJS  -  W  --   -           .       .   /   @CGY  -  L  --   -           .       .   /   @EDM  -  T  --   -           .       .   /    WAS  -  W  --   -          .       .   /    NYR  -  W  --   -          .       .   /   EDM  -  W  --   -          .       .     /   CGY  -  T  -- -          .       .   /  @BOS  -  W  --   -          .       .   /   DET  -  L  --   -          .       .   /   BOS  -  L  --   -          .       .   /  @NYI  -  L  --   -         .       .       /   HFD  -  W  --   -         . .   /  @PIT  -  L  --   -         .       .   /   @NYR  -  T  --   -         .       .   /    OTT  -  W  --   -         .       .   /   MTL  -  T  --   -         .       .     /  @NJD  -  L  --   -         .       .   /   NJD  -  L  -- -         .       .   /  @CGY  -  T  --  -         .       .   /  @VAN  -  W --  -         .       .   /  @MIN  -  L --  -         .       .   /   DET  -  - --  -         .       .   /    PIT  -  W --  -         .       .   /   @WAS  - W --  -         .       .     /   @NJD  -  L --  -        .       .   /   @NYI  -  L --  -        .       .   /   WAS  -  W --  -        .      .   /   MIN  -  W --  -        .      .   /  @PIT  -  L --  -        .      .   /   NJD  -  L --  -        .      .   /  @NYR  -  W --  -        .     .       /  @QUE  -  L --  -        .     .   /    LAK  -  L --  -        .     .   /    TOR  -  W --  -        .     .     ------------------------------------------------------------------------------- res=result, sh=shots, sv=saves GP=Games Played, MP=Minutes Played, GA=Goals Against, GAA=Goals Against Average SOG=Shots On Goal, SV=SaVes, SV%=SaVing Percentage, SO=ShutOuts, A=Assists -------------------------------------------------------------------------------  Staffan --  ((\\\\  //| Staffan Axelsson               \\\\  //|| etxonss@ufsa.ericsson.se     \\\\_))//-|| r.s.h. contact for Swedish hockey   '
# a sheet of special marks to drop
ListSpecialMarks = [ ':', ';', '[', ']', '{', '}', '~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '\\', '|', ',', '.', '/', '?', '\0', '<', '>', '\\', '\t', '\n', '\r', '\'', '\"', '\a', '\b', '\f', '\t', '\v', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']



# -------------------------------------------------------------------------------------------------
# a function to manually do word segmentation
def WordSeg(RawStr, AllLower = False ):
    """
    manually do word segmentation, return a list of strings;
    where :AllLower is a bool which decides if to convert all words to its lower case
    """
    CleanStr = ''  # after dropping special marks
    # 1. drop all recoreded special marks
    for tmpChar in RawStr:
        if tmpChar not in ListSpecialMarks:  # if current character is not in the list of special (useless) marks, push it to :CleanStr
            CleanStr += tmpChar
        else:
            CleanStr += ' '  # to prevent the @ mark in email addresses
    # 2. so, the next step is to drop extra whitespaces (>=2), only keeping 1 whitespace to divide every word
    CleanStr = CleanStr.split(' ')  # convert it to a list with many '' (empty string)
    # then, drop these elements of empty strings
    if AllLower:
        ListWd = [ x.lower() for x in CleanStr if x != '' ]
        return ListWd
    else:
        ListWd = [ x for x in CleanStr if x != '' ]
        return ListWd
    return None


# -------------------------------------------------------------------------------------------------
def GetIDF(NestedKwdLists,output=".\\output\\IDF.txt.big", IDFencoding="utf8"):
    """
    Compute IDF (inverse freq) and output to a pure text file (can be read by jieba package);
    requires a list of keyword-list like: [["a","b","c"],["A","C"]];
    where each element-list is a keyword list extracted from a single passage
    using collection module (std lib);
    no return;

    计算IDF，要求输入一个形如[["a","b","c"],["A","C"]]的列表，每个元素是从一篇文章里提取出来的关键字列表；没有返回值，输出jieba包能读取的IDF文件

    Pos Pars:
    1. NestedKwdLists [list of list of string]

    Kwd Pars:
    1. output [string]: file path to write, write mode if not exist (overwritten for each time if existing)
    1. IDFencoding [string]: encoding when writing IDF data to external file

    Returns:
    1. None

    Depends on;
    1. collections (std lib)
    2. codecs (std lib)

    the standard output file format, pls refer to: https://raw.githubusercontent.com/fxsjy/jieba/master/extra_dict/idf.txt.big
    """
    # 1. type assert
    assert isinstance(NestedKwdLists,list), "requires a list of lists of strings: NestedKwdLists, e.g. [[\"a\",\"b\"],[\"c\"]]"
    assert isinstance(output,str), "requires a list of string: output"
    # 2. loop in TextList, get counter objs for each element then store them in tmpVal
        # NOTE: collections.Counter obj is add-able, which means we can easily aggregate freqs in diff passages
        # NOTE: and it is a dict-like structure which can be traversaled by (key,value) pairs
    AggFreq = collections.Counter([])  # preprae a new collections.Couner instance
    for passage in NestedKwdLists:
        AggFreq += collections.Counter(passage)
    # 5. write to a pure text file, where each line: "keyword  freq"
        # NOTE: writing mode ("w") by default
    fio = codecs.open(output,"w", IDFencoding )  # use the same encoding as stopwords, utf8 by default
    for kwd,freq in AggFreq.items():
        fio.write(str(kwd))
        fio.write(" ")
        fio.write(str(freq))
        fio.write("\r\n") # NOTE: specially, pls use both \r\n rather than a single \n (or there will be failure when jba.set_idf_path() reads the output file)

    fio.close()
    # 6. logic return
    return None

def ReadIDF(IDFfilePath, IDFencoding='utf8'):
    """
    read in an IDF data file generated by the method GetIDF() above;
    returns a dictionary with keys (keyword) & values (counters)
    """
    # 1. open a file of reading
    tmpfile = codecs.open(IDFfilePath, 'r', encoding=IDFencoding)
    # 2. read the data line by line
    tmpList = tmpfile.readlines()
    # 3. pre-processing & add to the dictionary (pls note: the IDF data generated by :GetIDF() must have no repetition!)
    tmpDict = {}
    for tmpStr in tmpList:
        tmpStr = tmpStr.replace('\r\n','')
        tmpStr = tmpStr.split(' ')
        tmpDict[tmpStr[0]] = float(tmpStr[1])
    return tmpDict




# -------------------------------------------------------------------------------------------------
def Sampling4CV( IdxSet, fold = 5 ):
    """
    does sampling for N-fold cross validation;
    requires a set/collection (list or tuple) of the population of indices;
    the parameter :fold controls the number of folds to sampling;
    returns a list of lists, where every sub-list contains sampled indices;
    e.g. [[2,3],[1,4],[6,5],[8,7],[9,0]] for a 5-fold CV on an index population range(10)

    ## depends on
    1. random (std lib)
    """
    # 1. valdiation
    assert isinstance(fold, int), 'requires an integer: fold'
    # 2. get the sizes of each sampled group
    tmpStdSize = len(IdxSet) // fold   # standard size of groups
    tmpExtSize = len(IdxSet) % fold  # the size of the last group
    ListGroupSize = [ tmpStdSize for x in range(fold) ]
    if tmpExtSize != 0:   # if remained
        # NOTE: consider the case that the remainder is much smaller than the standard size of sample groups; 
        # a solution is to average the last two groups (where the very last group has the size :tmpExtSize) to make each group's size similar/closer
        tmpAvgSize = int( (tmpStdSize + tmpExtSize) / 2 )   # the int() constructor just take the integer part, similar to floor() but faster
        ListGroupSize[-2] = tmpStdSize + tmpExtSize - tmpAvgSize
        ListGroupSize[-1] = tmpAvgSize  # modify the very last element/group
    # 3. sampling
    IdxPopu = IdxSet.copy()  # get a copy of the population
    ListSamples = []
    for tmpSize in ListGroupSize:
        # 3.1 sampling for the current group, according to the group size recorded in :tmpSize
        tmpSample = random.sample(IdxPopu, tmpSize)
        # 3.2 drop selected element from the population
        for tmpIdx in tmpSample:
            IdxPopu.remove(tmpIdx)
        # 3.3 save the current sample group
        ListSamples.append(tmpSample)

    return ListSamples


# -------------------------------------------------------------------------------------------------
def unique( List ):
    """
    return a compact set/list (only unique elements) of input list :List
    """
    Res = [List[0]]
    for x in List:
        if x not in Res:
            Res.append(x)
    return Res



# -------------------------------------------------------------------------------------------------
def SVOPredInference( ListRealY, ListPredY, TrueValue = None ):
    """
    do inferences (I/II type errors) for predictions (2 groups);
    where :TrueValue requires a value (str or num) which indicates 'True' in :listRealY & :ListPredY
    return a dict;
    depends on unique() above
    """
    ResultDict = {}
    tmpZip = zip(ListRealY, ListPredY)  # if diff lengths, automatically raise an error
    tmpPopuSize = len(ListRealY)
    # 0. validation
    tmpUniqueRealY = unique(ListRealY)
    tmpUniquePredY = unique(ListPredY)
    assert len(tmpUniquePredY) <= 2, 'only supports 2-group classification: SVOPredInference(), but have true compact set '+str(tmpUniqueRealY)+' and predicted compact set '+str(tmpUniquePredY)
    # 1. select a true value
    assert (TrueValue in tmpUniquePredY) | (TrueValue in tmpUniqueRealY), 'invalid TrueValue: '+str(TrueValue)
    # 1. classification rate
    ResultDict['Classification Rate'] = sum([  r == p for r,p in tmpZip  ]) / tmpPopuSize
    ResultDict['Type I Error'] =   sum([  int((r == TrueValue) &  (r != p)) for r,p in zip(ListRealY, ListPredY)  ]) / tmpPopuSize
    ResultDict['Type II Error'] =  sum([  int((r != TrueValue) &  (r != p)) for r,p in zip(ListRealY, ListPredY)  ]) / tmpPopuSize
    ResultDict['True to True'] =   sum([  int((r == TrueValue) &  (r == p)) for r,p in zip(ListRealY, ListPredY)  ]) / tmpPopuSize
    ResultDict['False to False'] = sum([  int((r != TrueValue) &  (r == p)) for r,p in zip(ListRealY, ListPredY)  ]) / tmpPopuSize
    ResultDict['True Value'] = TrueValue

    return ResultDict

# sum(


