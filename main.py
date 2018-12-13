# Homework for the course: data mining
# (say no to extra 3rd-party packages!)
# -----------------------------------------
# 1. standard libraries
from os import listdir # directory operations
from os.path import isfile, join  # to operate file names & addresses (optional)
import collections  # a std lib about collection operations, esp. counting (for TF-IDF computing)
import codecs  # I/O for the files in variant encodings
# 2. modules wrote by myself
import funcs  # (homecook) word segmentation for English words, automatically delete common trash symbols/marks/characters (but not vocabularies)
# 3. 3rd party packages
from sklearn import svm  # to do classification through SVM


# -----------------------------------------
## environment variables
env = {
    'baseball' : './data/baseball/',
    'hockey' : './data/hockey/',
    'TrueValue' : 'baseball',  # select either 'baseball' or 'hockey' as the true value when computing type I/II errors
    'ReadEncoding' : 'utf-8',
    'StopWordListDir' : './data/StopWords.txt',  # the file location/directory/address of stop words
    'IDFdir' : './output/IDFdata.txt',  # trained IDF data (intermediate data, useful later)
    'fold' : 5, # numebr of folds in CV
}

## Section: Read in original text files to two groups
# -----------------------------------------
# 1. decalre two empty lists for the two groups in :env
DictRawText = {
    'baseball' : [],
    'hockey' : [],
}
# 2. a dictionary to record the name of every file (using the same key mappings as :DictRawText )
# NOTE: please make :DictTextName & :DictRawText have the same keys!!!!! (important)
DictTextName = {
    'baseball' : [],
    'hockey' : [],
}

# --------------------------------------------------------------------
# 1. read in the two groups of files in to a list of strings
for tmpKey in DictRawText.keys():
    # 1.1 get a name list of all data files
    DictTextName[tmpKey] = [ join(env[tmpKey], f) for f in listdir(env[tmpKey]) if isfile(join(env[tmpKey], f)) ]  # use isfile() to exclude possible folders
    # 1.2 read in files as a string
    for idx in range(len(DictTextName[tmpKey])):
        # 1.2.1 open the file and read in the WHOLE file as a string
        tmpStr = ''  # define a temp string
        try:
            with codecs.open(DictTextName[tmpKey][idx], 'r', encoding= env['ReadEncoding'] ) as tmpfile:
                tmpStr = tmpfile.read()
            # 1.2.2 save the temp string in to the list of original text
            DictRawText[tmpKey].append(tmpStr)
        except:
            print( 'Please check the encoding mode of the file: ' + DictTextName[tmpKey][idx] + ', the current encoding for read-in is ' + env['ReadEncoding'] )

print('-'*20)
print('+ Original files read; begin to do word segmentation ...')


# --------------------------------------------------------------------
# 2. word division (using the wordsegment package)
# 2.0 read in stop words in an external file as a list of string
tmpfile = codecs.open(env['StopWordListDir'], 'r', encoding= env['ReadEncoding'])
ListStopWords = tmpfile.readlines()
tmpfile.close()
ListStopWords = [ x.replace('\r','').replace('\n','').replace('\t','').strip() for x in ListStopWords ]  # cleaning/pre-processing the list of stopwords, drop extra/special characters
# 2.1 word segmentation
for tmpKey in DictRawText:
    for tmpMailIdx in range(len(DictRawText[tmpKey])):
        # NOTE: convert all words to their lower cases to avoid the differences between different cases, e.g. 'Fuck' & 'fuck'
        tmpWordList = funcs.WordSeg(DictRawText[tmpKey][tmpMailIdx], AllLower = True )  # a proposed/homecooked method to do English word segmentation (mainly drop special marks but no stop word); the :AllLower parameter indicates if to convert all words to their lower cases
        DictRawText[tmpKey][tmpMailIdx] = [ x for x in tmpWordList if x not in ListStopWords ]  # drop stop words
        # print('Word Segmented: '+DictTextName[tmpKey][tmpMailIdx] )  

# 2.2 print an info
print('+ All words in the Emails are segmented; begin to construct TF-IDF ...')


# --------------------------------------------------------------------
# 3. compute TF-IDF
# 3.1 prepare a joint list of the both groups (a nested list of list of keywords like: [['a','b'],['a','c'],['d','f]], each sublist)
# 3.1 prepare a joint list of the both groups (a nested list of list of keywords like: [['a','b'],['a','c'],['d','f]], each sublist)
ListTrainSet = []  # the value (texts) of every passage
ListTrainSetFileName = []  # the name/tags/ID/addresses of every passage
ListTrueClassFlag = []  # a list of strings, of flags of true classes for each passage, USED AS THE DEPENDENT VARIABLE IN SVM !!!
for tmpKey in DictRawText:
    for tmpMailIdx in range(len(DictRawText[tmpKey])):  # each :tmpMailIdx is the position of every passage/email
        ListTrainSet.append( DictRawText[tmpKey][tmpMailIdx] )
        ListTrainSetFileName.append( DictTextName[tmpKey][tmpMailIdx] )
        ListTrueClassFlag.append( tmpKey )

# 3.2 compute IDF based on the whole training set (both the groups), then output the IDF data (not normalized) to an external file
funcs.GetIDF(ListTrainSet, output=env['IDFdir'], IDFencoding=env['ReadEncoding'] )
# 3.3 read in the IDF data as a dictionary (pls note: just countings, not final IDF weights!)
tmpDictIDF = funcs.ReadIDF(env['IDFdir'], IDFencoding=env['ReadEncoding'] )
# 3.4 compute IDF weights (weights = number of all passages / counting of each keyword )
tmpSum = len(ListTrainSet)  # the total numebr of passages/emails
for tmpKey,tmpVal in tmpDictIDF.items():
    tmpDictIDF[tmpKey] = tmpSum / tmpVal  # get IDF weights

# 3.5 compute TF-IDF for each passage
# NOTE: using a list of dict e.g. [{'word':TF-IDF,'word':TF-IDF},{},{}] to store the results
ListTFIDF = []
for tmpPassageWordList in ListTrainSet:
    # 3.5.1 count the frequency of every word in :tmpPassage, convert it to a dict
    tmpTF = dict( collections.Counter(tmpPassageWordList) )
    # 3.5.2 compute TF-IDF = IDF weights * TF of every word
    for tmpKey,tmpVal in tmpTF.items():
        tmpTF[tmpKey] = tmpDictIDF[tmpKey] * tmpVal  # pls NOTE: the :tmpDictIDF & :tmpTF shares a common union of keys
    # 3.5.3 store the temp dictionary of TF-IDF to :ListTFIDF
    ListTFIDF.append( tmpTF )

print('+ TF-IDF constructed; begin to construct feature vectors ...')



# --------------------------------------------------------------------
# 4. construct feature vectors/points for each passage/email
# 4.1 get the length of the feature vectors (using the number of the union of all unique words in the whole training set)
# NOTE: about 18504 in my answer
FeatureDim = len(tmpDictIDF.keys())  
# 4.2 construct a template vector which maps every word to its position in the final feature vectors
FeatVecTemplate = list(tmpDictIDF.keys()) # just using the random/laten/underlying order of the keys of :tmpDictIDF
# 4.3 now, loop to construct feature vectors for each passage/mail, where intercepts on every dimension is the value of TF-IDF of the corresponding word in the union set of words （不是人话凑合着看）
ListFeatVec = []
for tmpPassageTFIDFDict in ListTFIDF:
    # 4.3.0 preprae a temp vector/list for the current passage
    tmpFeatVec = [ 0 for x in range(FeatureDim) ]  # though the :FeatVecTemplate consists of strings, we can easily replace them with numbers (TF-IDF values)
    for tmpKey,tmpVal in tmpPassageTFIDFDict.items():
        # 4.3.1 get the current word's position in the template feature vector
        # NOTE: we have learned that there is no repetition in :FeatVecTemplate, so the result of [].index() methods is unique for every word
        try:
            tmpLoc = FeatVecTemplate.index( tmpKey )
        except:
            print('Failed to Fill: '+tmpKey)
        # 4.3.2 write TF-IDF value to the :tmpFeatVec
        tmpFeatVec[tmpLoc] = tmpVal
    # 4.3.3 store the temp vector (feature vector) of each passage/email into :ListFeaVec
    ListFeatVec.append( tmpFeatVec )

print('+ Feature vectors constructed; begin to train the SVO model; may take time ...')



# --------------------------------------------------------------------
# 5. using SVM to do classification
# NOTE: because we only have two latent classe, therefore, just use SVC to do classification
# NOTE: the regressor martrix X = ListFeatVec (size: number of passages * dim of feature vectors, not converted to a numpy matrix but in a simple nested list ), and the dependent variable vector Y = ListTrueClassFlag (len = number of passages)
# 5.1 create an isntance of SVC model, then fit the model
clf = svm.SVC()
# 5.2 training
clf.fit( ListFeatVec, ListTrueClassFlag )
print('+ SVO trained; begin to evaluate in-sample predictions; may take time ...')
# 5.3 in-sample prediction
tmpInSamplePredict = clf.predict(ListFeatVec)
print('+ SVO In-sample Predicted')
# 5.4 Inferences (I, II types of errors)
tmpSVOInference = funcs.SVOPredInference( ListTrueClassFlag, tmpInSamplePredict, TrueValue = env['TrueValue'] )
# 5.5 display
print('+ Estimation Results:')
for tmpKey,tmpVal in tmpSVOInference.items():
    print('\t- '+tmpKey+' : '+str(tmpVal)  )





# --------------------------------------------------------------------
# 6. 5-fold CV
# 6.1 get the sampled indices groups to slice the samples, a list of lists
ListCVSampleIdxSet = funcs.Sampling4CV( list(range(len(ListTrainSet))), fold = env['fold'] )
# 6.2 prepare a dict of data pair/tuple like [(TrainSetList,PrediSetList),(),(),(),()]
DictCVResult = {
    'TrainX' : [],  # a list of training dataset of each fold (each element is a list/datavector)
    'TrainY' : [], # a list of predicting dataset of each fold
    'PredX' : [],  # a list of training outcomes of each fold
    'PredYReal' : [],  # a list of the real values of predicting sets' outcomes
    'PredictedY' : [],  # predicted Y of the predicting set
    'Inferences' : [],  # a list of dicts of inferences for each fold's model
}
for tmpCVIdxSet in range(len(ListCVSampleIdxSet)):
    # 6.2.1 prepare data
    tmpCopyIdxSet = ListCVSampleIdxSet.copy()
    tmpIdxSetPred = tmpCopyIdxSet.pop(tmpCVIdxSet)  # index set of current prediction set
    tmpIdxSetTrain = []  # an index set of current training set
    for tmp in tmpCopyIdxSet:
        tmpIdxSetTrain.extend(tmp)
    # 6.2.2 slice data
    tmpTrainX = [ ListFeatVec[x] for x in tmpIdxSetTrain ]
    tmpTrainY = [ ListTrueClassFlag[x] for x in tmpIdxSetTrain ]
    tmpPredX = [ ListFeatVec[x] for x in tmpIdxSetPred ]
    tmpPredY = [ ListTrueClassFlag[x] for x in tmpIdxSetPred ]
    DictCVResult['TrainX'].append( tmpTrainX )
    DictCVResult['PredX'].append( tmpPredX )
    DictCVResult['TrainY'].append( tmpTrainY )
    DictCVResult['PredYReal'].append( tmpPredY )
# 6.3 do CV
print('+ begin to estimate models for '+str(env['fold'])+'-fold CV ...')
for tmpCV in range(env['fold']):
    # 6.3.1 estimation
    tmpclf = svm.SVC()
    tmpclf.fit( DictCVResult['TrainX'][tmpCV], DictCVResult['TrainY'][tmpCV] )
    print('\t- Estimated Model '+str(tmpCV))
    # 6.3.2 prediction (out-sample)
    DictCVResult['PredictedY'].append( tmpclf.predict( DictCVResult['PredX'][tmpCV] ) )
    print('\t- Predicted Model '+str(tmpCV))
    # 6.3.3 inferences
    DictCVResult['Inferences'].append( funcs.SVOPredInference( DictCVResult['PredYReal'][tmpCV], DictCVResult['PredictedY'][tmpCV], TrueValue=env['TrueValue'] ) )
    print('\t- Inferences for Model '+str(tmpCV))

print('+ Cross Validation Done')
# 6.5 aggregate the data of CV inferences
tmpDictCVAgg = {}
tmpDictCVAgg['Average Classification Rate'] = sum([  x['Classification Rate'] for x in DictCVResult['Inferences']  ]) / env['fold']
tmpDictCVAgg['Average Type I Error (True to False)'] = sum([  x['Type I Error'] for x in DictCVResult['Inferences']  ]) / env['fold']
tmpDictCVAgg['Average Type II Error (False to True)'] = sum([  x['Type II Error'] for x in DictCVResult['Inferences']  ]) / env['fold']
tmpDictCVAgg['Average True to True'] = sum([  x['True to True'] for x in DictCVResult['Inferences']  ]) / env['fold']
tmpDictCVAgg['Average False to False'] = sum([  x['False to False'] for x in DictCVResult['Inferences']  ]) / env['fold']
tmpDictCVAgg['True Value'] = env['TrueValue']
# 6.6 display the results of CV
print('+ Results of '+str(env['fold'])+'-fold Cross Validation:' )
for tmpKey,tmpVal in tmpDictCVAgg.items():
    print('\t- '+tmpKey+' : '+str(tmpVal))










