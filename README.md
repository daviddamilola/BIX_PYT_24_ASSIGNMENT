# Fastqc Reporter Technical

# Documentation


## TableOf Contents

- Introduction..................................................................................................................................
- Installation....................................................................................................................................
- ProgramDesign...........................................................................................................................
   - OverviewofFunctionality...................................................................................................
- FolderStructure...........................................................................................................................
- DependenciesUsed...................................................................................................................
- ExampleUsage..........................................................................................................................
   - OptionsandResults.........................................................................................................
      - PerTileSequenceQualitySection............................................................................
         - PlotOutput:..........................................................................................................
         - Interpretation:.......................................................................................................
      - PerSequenceQualityScoresSection.......................................................................
         - Plotoutput............................................................................................................
         - Interpretation:.......................................................................................................
      - PerbasesequencecontentSection..........................................................................
         - Plotoutput:...........................................................................................................
         - Interpretation:.......................................................................................................
      - PersequenceGCcontentSection.............................................................................
         - Interpretation:.......................................................................................................
         - Plotoutput............................................................................................................
      - PerbaseNcontentSection.......................................................................................
         - Interpretation:.......................................................................................................
         - Plotoutput............................................................................................................
      - SequenceLengthDistributionSection.......................................................................
      - SequenceDuplicationLevelsSection........................................................................
         - Plotoutput:...........................................................................................................
      - Overrepresentedsequencessection.........................................................................
      - AdapterContentSection............................................................................................
         - Interpretation:.......................................................................................................
         - Plotoutput:...........................................................................................................
      - K-merContentSection...............................................................................................
         - Interpretation:.......................................................................................................
         - Plotoutput:...........................................................................................................
- ErrorHandling............................................................................................................................
- References.................................................................................................................................


## Introduction..................................................................................................................................

FastqcreporterisaCommandLineInterface(CLI)toolbuilttoparsefastqcfilesintothe
availablesectionsandgeneratereportscontainingthesectioncontents.Italsogeneratesa
graphicalrepresentationofthesectionandaflagfilecontainingtheresultoftheQCtest,which
canbethevaluespass,fail,orwarn.

## Installation....................................................................................................................................

Torunthisprogram,thefollowingarerequired;

```
● FromPython3.9upwards.
● Condaorvenv(condaisusedforthescriptinthisdocumentation).
```
Thenextstepistocreateanewvirtualenvironmentandinstallthedependencies.

>>$ conda create -c conda-forge -n name_of_my_env seaborn pandas
matplotlib

Thiswillcreateacondaenvironmentandinstalltheseaborn,pandas,andmatplotlib
dependencies.Afterwards,activatethevirtualenvironmentbydoing;

>>$ source activate name_of_my_env

Finally,runtheprogramwithitsrequiredparametersandoptionalparameters.SeetheExample
Usagesectionformoreinfo.

## ProgramDesign...........................................................................................................................

Fastqcreportertakesanobject-orientedapproachtoparsingfastqcfilesandgenerating
appropriatereportsandgraphs.Twomainclassesexist;

```
● FastQCParser
● Section
```
The FastQCParser class encapsulatesthefunctionalitiesofparsingthefastqcfilesinto
sectionsanddefinesthemethodstohandlethesupportedoptionalparameterswhenpassed.

TheSection classencapsulatesthefunctionalitiesofwritingeachsection’sreportandflagfile
toitsappropriatefolderdependingontheoptionalparameterspassed.


EachsectionhasitsclassandinheritsfromthebaseSectionclass.Allthepropertiesofthe
sectionclassareinheritedanditnowdefinesitsimplementationoftheplot_section()
method.Thismethodplotsthenecessarygraphthatsuitsthetypeofdatathesectioncontains.

ThedataineachsectionisrepresentedinternallyasaPythondictionary,wherethekeys
representthetitleofeachsectionandthevaluesareanotherdictionaryhavingthesection
contentandthefastqcteststatus.

Adictionarywasusedastheinternaldatastructurebecauseitenablesustoparsethefileonce
intomemoryandpickeachsectioneffortlessly.

### OverviewofFunctionality...................................................................................................

Fastqcreportermakesuseoftheargparse modulefromPythontoaddadescriptionofwhat
thetoolisfor.Italsoaddsalistofparameters.Twoparametersarerequiredtorunthescript;

```
● Thepathtothefastqcfile
● Thefoldertooutputtheplots,reports,andflag
```
Otheroptionalparametersaredefinedviatheadd_argument methodoftheargparse
module.Theyareoptionalbecausetheactionparameterissettostore_true,whichsaves
themifavailable.

TheFastQCParser Classisinstantiatedwiththetworequiredparameters,andanempty
dictionaryiscreated.Theparse_fastqc_to_dictionary()methodoftheclassiscalledto
readthefile,andeachsectionissavedintothedictionarywiththesectiontitleasthekey.


**Figure2:** Flowchartdiagramfortheparse_fastqc_to_dictionary()method.

Theprogramthencheckstoseeifanyoptionalargumentsarepassedinthecommandlineand
callstheappropriatemethodtohandleit.TheFastQCParser classdefinesmethodsto
handleallthesections.

Theconceptdiagramillustratingthestructureoftheprogramisshownbelow.


**Figure3:** FlowchartdiagramforFastqcreporterprogram.


**Figure4:** ClassdiagramfortheFastQCParserclassshowingitsattributesandmethodsto
handlesectionsofthefastqcfile.

Allthemethodsforeachoptiondothefollowing;

```
● CreatetheappropriateSectionclass.
● Writetherequiredoutputs(report.txt,flag.txt,plot.png)tothefolderspecified.
```
Thebasestatisticsarealwaysprintedtotheconsole,regardlessofthesectionthatisrun.This
ispossiblebecauseofthestaticmethodprint_summary().

Toseethelistofoptions,passthe-hor--help optiontothefastqc_reporterscript.

**Terminal**
>>$ python3 fastqc_reporter.py ./data/fastqc_data1.txt ./solution1/
-h


**Output**

**Figure5:** Theoutputofrunningthehelpoptiontofastqc_reporter

EachsectioniscreatedfromthebaseclassSection. Thisclassdefinesattributesand
methodstocreateareport.txtfileandflag.txtfile.

```
Figure6: ClassdiagramfortheSectionclass
```
IndividualsectionsthenextendtheSection class andaddamethodtoplotthegraphsbased
onthesectiondata.


**Figure7:** ClassdiagramfortheModelspackagedepictinginheritanceperspecificsection.

## FolderStructure...........................................................................................................................

Thefastqcreporterisstructuredintofourmainfilesandfolders;

```
● Themodelfolder.
● Theconstants.pyfile.
● Thefastqc_reporter.pyfile.
● Thedatafolder.
```
Theentrypointisthefastqc_reporter.py file,itdefinesalltheparseroptionsandcallsthe
appropriatefunctiontohandletheoptionspassed.ItusestheFastQCParser classtocreate
theparserinstancetohandletheoptionsprovided.


Theconstants.py file createsthetitlesofeachsection.Thisisnecessaryformaintainability
asitletsushaveasinglepointtochangethetitlesifneededsincetheyareusedinseveral
placesacrosstheprogram.

Themodelfoldercontainsalltheclassesusedinthescript.Itispackagedasamodulewiththe
__init__.pyfile,withthis,the fastqc_reporter.py filecanaccessalltheclasses
underthemodel namespace.

Thedatafoldercontainstheexampletestfastqcfilesusedtotestthefunctionalityofthe
fastqc_reporter.pyscript.

Thepicturebelowshowsthefolderstructureforthecorefunctionalityofthefastqcreporter.

**Figure8:** Imageshowingthefolderstructureforthefastqcreporterscript.


## DependenciesUsed...................................................................................................................

MatplotlibwasusedtogetherwithSeaborntoplotthegraphsforeachsection.Seaborn’s
plottingfunctionswereusedfordifferentkindsofplotsasappropriate(SeabornDocumentation,
n.d.).

PandasLibrarywasusedtoextractthedataineachsectionintoadataframe.The
pandas.read_csv()methodwasusedtoreadthereport.txtfilesintoadataframe.(Pandas
Documentation,n.d.).

## ExampleUsage..........................................................................................................................

Aftersettinguptheenvironmentandinstallingthenecessarydependencies,theprogramcanbe
runinitsdefaultformlikethis;

>>$ python3 fastqc_reporter.py ./data/fastqc_data1.txt ./solution1/

Thefirstparameteristhepathtothefastqcfileandthesecondistheoutputfolderpath.The
resultofthebasestatisticsisprintedtotheconsole.

$>>Basic Statistics pass

#Measure Value
Filename 4_age21_S12_L001_R2_001_concat.fastq.gz
File type Conventional base calls
Encoding Sanger / Illumina 1.
Total Sequences 37287903
Sequences flagged as poor quality 0
Sequence length 75
%GC 55
>>END_MODULE

### OptionsandResults.........................................................................................................

Therearedifferentoptionspersection.Theusercanpassanoptionormultipleoptionsto
specifywhichsectiontorun,alsotheusercanpassthe-aor--alloptiontoprocessallthe
sections.

Theresultsinthisreportwereforthefastqctestfile(fastqc_data1.txt)locatedinthedata
folder.Theoutputsweresavedtothesolution1folder.

Foreachrun,thebasicstatisticsarealwaysprintedtotheconsole;


$>>Basic Statistics pass

#Measure Value
Filename 4_age21_S12_L001_R2_001_concat.fastq.gz
File type Conventional base calls
Encoding Sanger / Illumina 1.
Total Sequences 37287903
Sequences flagged as poor quality 0
Sequence length 75
%GC 55
>>END_MODULE

#### PerTileSequenceQualitySection............................................................................

Option: -t or --per_tile_seq_qual

##### PlotOutput:..........................................................................................................

**Figure9:** Heatmapshowingtheper-tilesequencequalityacrossbasepositions.


##### Interpretation:.......................................................................................................

##### Interpretation:.......................................................................................................

Theplotshowsthatthemeanqualityscoresacrossthetilesarehighandconsistent.However,
therearepatchesofbluewhichindicatethelowerqualityregions.Thiscanresultfromsystemic
issueswiththosetilesorerrorsintroducedduringsequencing(BabrahamInstitute,n.d.).

#### PerSequenceQualityScoresSection.......................................................................

Option: -s or --per_seq_qual_scores

##### Plotoutput............................................................................................................

**Figure10:** Barplotshowingtheper-tilesequencequalityacrossbasepositions.

Interpretation:

Thedistributionofthequalityscoresishighlyskewedtotheright,indicatingthatmostreadsare
highquality.Aqualityscoreof 40 indicatesveryconfidentbasecallswithaverylowprobability
oferror.Phredsscoreof 40 correspondstoanerrorprobabilityof0.0001(O'Raweetal.,2015).


#### PerbasesequencecontentSection..........................................................................

Option: -c or --per_base_seq_content

##### Plotoutput:...........................................................................................................

**Figure11:** LinePlotshowingtheper-basesequencecontentacrossbasepositions.

##### Interpretation:.......................................................................................................

##### Interpretation:.......................................................................................................

Accordingtotheplotabove,thereisaslightlyhigherpercentageofGandCcomparedtoAand
Tthroughoutthereadlength.DependingontheexpectedGCcontentofthetargetgenomeor
transcriptome,thiscouldindicateaGCbiasinthelibrarypreparationorsequencing.(Illumina,
2018)

#### PersequenceGCcontentSection.............................................................................

Option: -g or --per_seq_GC_cont


##### Interpretation:.......................................................................................................

Accordingtotheplotbelow,TheGCcontentdistributionishighestaround55-60%,whichmay
indicatethatmostreadshaveaGCcontentinthisrange.TheGCcontentdistributionis
relativelysymmetric,indicatingthatthelibrarypreparationandsequencingprocesseswere
successful,withminimalGC-relatedbias.(Illumina,2018)

##### Plotoutput............................................................................................................

**Figure12:** LinePlotshowingtheper-sequenceGCcontentdistributionacrossbasepositions.

#### PerbaseNcontentSection.......................................................................................

Option: -n or --per_base_N_cont

Interpretation:

Thelineplotstartswithaspikeatbaseposition1.Aftertheinitialbase,theNcontentdropsto
almost0%andremainsconsistentlylow,indicatinggoodsequencingqualityfortherestofthe
read.


Trimmingcanbeemployedforthefirstbasefromeachreadtoimprovetheoverallqualityofthe
dataandensureoptimalperformanceindownstreamanalyses.

##### Plotoutput............................................................................................................

**Figure13:** LinePlotshowingtheperbaseNcontentdistributionacrossbasepositions.

#### SequenceLengthDistributionSection.......................................................................

Option: -l or --seq_len_dist
Plotoutput:NotApplicable

#### SequenceDuplicationLevelsSection........................................................................

Option: -d or --seq_dup

Interpretation:

Intheplotbelowaround 70%ofthereadsareunique,whichisgoodintermsoflibrarydiversity.
Thereisanoticeablelevelofduplication,withaspikeinthe>10duplicationcategory,
suggestingpotentialPCRamplificationbias.(Akalin,2020).


##### Plotoutput:...........................................................................................................

**Figure14:** BarPlotshowingthesequenceduplicationleveldistribution.

#### Overrepresentedsequencessection.........................................................................

Option: -o or --over_seq
Plotoutput: NotApplicable

#### AdapterContentSection............................................................................................

Option: -p or --adap_cont

##### Interpretation:.......................................................................................................

TheplotbelowshowsthattheIlluminaUniversalAdapterispresentinasmallbutincreasing
percentageofreadstowardtheendofthesequences.

Theremainingadaptertypes(IlluminaSmallRNAAdapter,NexteraTransposaseSequence,
andSOLIDSmallRNAAdapter)havelittletonopresence,whichindicatesthatthereiseffective
trimmingorthattheadaptersaretotallyabsent.

Usingadaptertrimmingtools(e.g.Btrim)isrecommendedtoimprovethequalityofthedataand
ensurethatthedatasetisreadyforfurtherprocessingwithoutbiasorartifacts.(Kong,2011).


##### Plotoutput:...........................................................................................................

**Figure15:** LineplotshowingtheAdaptercontentacrosspositions.

#### K-merContentSection...............................................................................................

Option: -k or --kmer_count

##### Interpretation:.......................................................................................................

Theplotindicatesthatcertaink-mers,suchasCCCACGTandCGGGCAT,arehighly
over-represented,withcountsexceeding10,000occurrences.

Thisover-representationcouldindicateadaptercontamination,PCRbias,orlowlibrary
complexity.(Akalin,2020).


##### Plotoutput:...........................................................................................................

**Figure16:** LineplotshowingtheKmercontentacrosspositions.

**AllSections**
Option: -a or --a
Plotoutput:runsalltheplotsforeachsectionwhereapplicable,asdescribedabove.

## ErrorHandling............................................................................................................................

ErrorswerehandledwiththenativePythontry: exceptconstruct.Errorsthatmayarisefrom
baduserinput,malformedfastqcfiledata,filewritingpermissions,andfileparsingarehandled
appropriately.

Theprogramwillexitwithanon-zeroexitcodeifitencountersanerrorandwillprinttheerrorto
theconsole.


## References.................................................................................................................................

Akalin,A.(2020). _ComputationalgenomicswithR_
(Chapter7:Qualitycheck,processingandalignmentofhigh-throughputsequencing
reads).Bookdown.
https://compgenomr.github.io/book/quality-check-on-sequencing-reads.html

BabrahamInstitute.(n.d.).
_FastQCpertilesequencequalityanalysis_.
https://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/3%20Analysis%20Modu
les/12%20Per%20Tile%20Sequence%20Quality.html

Kong,Y.(2011).
Btrim:Afast,lightweightadapterandqualitytrimmingprogramfornext-generation
sequencingtechnologies. _Genomics, 98_ (2),152-153.
https://doi.org/10.1016/j.ygeno.2011.05.

Illumina.(2018,September26).
_Askascientist-WhatisGC-Bias?_ [Video].YouTube.
https://www.youtube.com/watch?v=wdEb3chYFOw

O'Rawe,J.F.,Ferson,S.,&Lyon,G.(2015,February1).
AccountingforuncertaintyinDNAsequencingdata. _TrendsinGenetics, 31_ (2),61–66.
https://doi.org/10.1016/j.tig.2014.12.

PandasDocumentation.(n.d.).
_pandas.read_csv_ .In _Pandasdocumentation_.
https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html#pandas.read_csv

SeabornDocumentation.(n.d.).
_Overviewofseabornplottingfunctions_ .In _Seaborndocumentation_.
https://seaborn.pydata.org/tutorial/function_overview.html


