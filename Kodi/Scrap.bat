@echo off & setlocal enabledelayedexpansion
set Basefolder="J:\infomercial"
REM Based on the idea and script by 2Flower http://forum.xbmc.org/showthread.php?tid=153253
REM ====== Instructions ======
REM Just change the path of the folder above and to the one where you keep all your unscrapeable videos you wish to have .nfo files generated for. 
REM Please do not let this script run over your existing, scrapeable tv series folder! Use a separate one instead!
REM I highly recommend to create one folder per "show" and to avoid subfolders below that in order to achieve a clean, working structure in the XBMC database.
REM After running this script, go into XBMC, add your folder as a new source to your database and set the type to "tv series". Please make sure to choose a tv series scraper as well though it will take the information just from the .nfo files you just generated.

echo Creating a .nfo files for each new video. The last used episode 
echo number will be stored in the episodecounter.txt for the next time.
echo ---------------------------------------------------------------------------
pushd %Basefolder%
echo Scanning for new videos in %Basefolder%
for /f "delims=" %%f in ('dir /b /s /O:N *.mp4 *.avi *.mkv *.wmv *.flv *.webm *.m4v *.ts') do (
pushd "%%~dpf"
REM Checking whether a folder contains video files and whether it already contains an episode counter file. If not it generates one starting with zero.
if not exist episodecounter.txt (
  echo 0 > episodecounter.txt
)
REM Checking for (new) video files without according .nfo
if not exist "%%~nf.nfo" (
REM Using the last known episode number in each folder and sets it +1.
set /p "Episode=" < episodecounter.txt
set /A Episode +=1
REM Getting the creation date of the video file, splits it up and uses it as air date.
set "timestamp=%%~tf"
set "month=!timestamp:~3,2!"
set "year=!timestamp:~6,4!"
set "day=!timestamp:~0,2!"

REM Just for the looks... If the episode number is below 10 it adds an zero to get e.g. s01e05 instead of s01e5
if !Episode! LSS  10 (
  REM Writing a basic XML structure to the according .nfo just using the file name as a title.
  echo ^<tvshow^>^<title^>%%~nf^</title^>^<plot^>%%~nf^</plot^>^</tvshow^> > %%~nf.nfo
  REM Renaming the video file by adding season and episode, e.g. "orginialfilename.s01e08.avi"
  rename "%%~nxf" "%%~nf%%~xf"
  echo Renamed and added .nfo for "%%~nf.s01e0!Episode!"
) else (
  echo ^<tvshow^>^<title^>%%~nf^</title^>^<plot^>%%~nf^</plot^>^</tvshow^> > %%~nf.nfo
  rename "%%~nxf" "%%~nf%%~xf"
  echo Renamed and .nfo for "%%~nf"
)
REM Writes the last used episode number into a .txt for later use
echo !Episode! > episodecounter.txt
)
)
echo Done.
echo ---------------------------------------------------------------------------
echo Creating tvshow.nfo files using the name of the folder as show title
echo ---------------------------------------------------------------------------
pushd %Basefolder%
echo Scanning for new folders in %Basefolder%
for /f "delims=" %%f in ('dir /b /s /O:D *.mp4 *.avi *.mkv *.wmv *.flv *.webm *.m4v *.ts ') do (
pushd "%%~dpf"
REM Getting the name of the parent folder for each video file. Empty folders will be ignored.
FOR %%A IN (.) DO (
  REM Checking whether there is a .nfo file yet. If not it generates one.
set "timestamp=%%~tf"
set "month=!timestamp:~3,2!"
set "year=!timestamp:~6,4!"
set "day=!timestamp:~0,2!"
  if not exist "%%~dpftvshow.nfo" (
   echo New folder "%%~nA" found! tvshow.nfo generated
   REM Writing a basic XML structure to the tvshow.nfo just using the folder name as a title.
   echo ^<tvshow^>^<title^>%%~nA^</title^>^<premiered^>!year!-!month!-!day!^</premiered^>^<season^>1^</season^>^</tvshow^> > %%~dpftvshow.nfo
   )
  )
)
echo Done.
endlocal