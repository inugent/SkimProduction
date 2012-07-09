#! /usr/bin/perl
use Cwd;
use POSIX;
#############################################
$numArgs = $#ARGV +1;
$ARGV[$argnum];

if($ARGV[0] eq "--help" || $ARGV[0] eq ""){
    printf("\nThis code requires one input option. The systax is:./todo.pl [OPTION]");
    printf("\nPlease choose from the following options:");
    printf("\n\n./todo.pl --help                                   Prints this message");
    printf("\n\n./todo.pl --Submit <python_cfg> <InputPar.txt>     Submit crab jobs to the grid");
    printf("\n                                                   <InputPar.txt> contains input command template.");
    printf("\n                                                   Option: --n number of jobs to submit [njobs=0 by default].");
    printf("\n                                                   PLEASE: run a test with --n 0 and then --n 1 before production.");
    printf("\n\nNotes: The <InputPar.dat> format requires 1 input per line where datasetpath = <datasetpath> start a new dataset.");
    printf("\nThe current input options are:");
    printf("\n    DataType = <DataType>");
    printf("\n    datasetpath = <datasetpath>");
    printf("\n    dbs_url = <dbs_url>");
    printf("\n    publish_data_name = <publish_data_name>");
    printf("\n    output_file = <output_file>");
    printf("\n    lumi_mask = <lumi_mask>");
    printf("\n    total_number_of_lumis = <total_number_of_lumis>");
    printf("\n    total_number_of_events = <total_number_of_events>");
    printf("\n    number_of_jobs = <number_of_jobs>");
    printf("\n    CE_white_list = <CE_white_list>");
    printf("\nList of DataTypes:\n");
    printf("    data, h_tautau, hpm_taunu, ttbar, w_lnu, w_enu, w_munu, w_taunu, dy_ll, dy_ee, dy_mumu, dy_tautau\n");
    printf("    ZZ, WW, WZ, qcd\n");
    printf("\n\n./todo.pl --SkimSummary <InputPar.txt> <CodeDir> Produces the SkimSummary.log to summarize the skim information."); 
    printf("\n                                                   This is run after retreiving the output from the job. The output");
    printf("\n                                                   goes in Code/InputData/.\n");
    printf("\n./todo.pl --CheckandCleanOutput <InputPar.txt>     Checks number fo output files (crab can produce duplicate files when resubmitting)");
    printf("\n                                                   OutputFilesfromDisk.log - List of output Files on Disk.");
    printf("\n                                                   OutputFilesfromlog.log - List of output Files from log files.");
    printf("\n                                                   DiffLogAndDisk.log - List of files which are on Disk but not in log files"); 
    printf("\n\n");
    exit(0); 
} 

######################################
$InputFile=$ARGV[1];
$njobs=0;
for($l=3;$l<$numArgs; $l++){
    if($ARGV[l] eq "--n"){
	$l++;
	$njobs=$ARGV[l];
    }
}


if( $ARGV[0] eq "--Submit" ){

    #organize the Lumi_XYZ.root file
    system(sprintf("mkdir ../../data"));    
    system(sprintf("cp  ../../TauDataFormat/TauNtuple/Cert_PU_FILES/Lumi_160404_180252_andMC_Flat_Tail.root ../../data/ "));
    system(sprintf("rm createandsubmit_test; touch createandsubmit_test"));
    system(sprintf("rm createandsubmit; touch createandsubmit"));
    system(sprintf("rm getoutput; touch getoutput"));    
    $pythonfile=$ARGV[1];
    $TempDataSetFile=$ARGV[2];
    # Open ListofFile.txt
    @datasetpath;
    @dbs_url;
    @publish_data_name;
    @output_file;
    @lumi_mask;
    @total_number_of_lumis;
    @total_number_of_events;
    @number_of_jobs;
    @CE_white_list;
    @CE_black_list;
    @DataType;
    @globaltag;
    open(DAT, $TempDataSetFile) || die("Could not open file $TempDataSetFile! [ABORTING]");
    $idx=-1;
    while ($item = <DAT>) {
	chomp($item);
	($a,$b,$c,$d)=split(/ /,$item);
	if($a eq "DataType"){
	    $idx++;
	    push(@datasetpath,"");
	    push(@dbs_url,"");
	    push(@publish_data_name,"");
	    push(@output_file,"");
	    push(@lumi_mask,"");
	    push(@total_number_of_lumis,"");
	    push(@total_number_of_events,"");
	    push(@number_of_jobs,"");
	    push(@CE_white_list,"");
	    push(@CE_black_list,"");
	    push(@DataType,$c);
	    push(@globaltag,"");
	}
        if($a eq "process.GlobalTag.globaltag"){
            $globaltag[$idx]=$item;
        }
        if($a eq "datasetpath"){
            $datasetpath[$idx]=$item;
        }
	if($a eq "dbs_url"){
	    $dbs_url[$idx]=$item;
	}
        if($a eq "publish_data_name"){
            $publish_data_name[$idx]=$item;
	}
	if($a eq "output_file"){
	    $output_file[$idx]=$item;
	}
	if($a eq "lumi_mask"){
	    $lumi_mask[$idx]=$item;
	}
	if($a eq "total_number_of_lumis"){
	    $total_number_of_lumis[$idx]=$item;
	}
	if($a eq "total_number_of_events"){
	    $total_number_of_events[$idx]=$item;
	}
	if($a eq "number_of_jobs"){
	    $number_of_jobs[$idx]=$item;
	}
	if($a eq "CE_white_list"){
	    $CE_white_list[$idx]=$item;
	}
	if($a eq "CE_black_list"){
            $CE_black_list[$idx]=$item;
        }

    }
    close(DAT);
    ## create crab files and submit 
    $idx=0;
    foreach $data (@DataType){
	$dir=$DataType[$idx];
	$dir=~ s/.root/_CRAB/g;
	$dir=~ s/DataType =/ /g;
	$dir.=sprintf("%d", $idx);
	printf("\ncreating dir: $dir\n");
	system(sprintf("rm $dir -rf; mkdir $dir; cp crab_TEMPLATE.cfg  $dir/crab.cfg;cp $pythonfile $dir/HLT_Tau_Ntuple_cfg.py"));
	system(sprintf("cp ../../data/Lumi_160404_180252_andMC_Flat_Tail.root $dir"));
	system(sprintf("./subs \"<DataType>\"               \"$DataType[$idx]\"                      $dir/HLT_Tau_Ntuple_cfg.py"));
	system(sprintf("./subs \"<globaltag>\"               \"$globaltag[$idx]\"                    $dir/HLT_Tau_Ntuple_cfg.py"));
	system(sprintf("./subs \"<datasetpath>\"            \"$datasetpath[$idx]\"                   $dir/crab.cfg"));
	system(sprintf("./subs \"<dbs_url>\"                \"$dbs_url[$idx] \"                      $dir/crab.cfg"));
	system(sprintf("./subs \"<publish_data_name>\"      \"$publish_data_name[$idx] \"            $dir/crab.cfg"));
	system(sprintf("./subs \"<output_file>\"            \"$output_file[$idx] \"                  $dir/crab.cfg"));
	if($lumi_mask[$idx] ne "none"){
	    $lumifile=$lumi_mask[$idx];
	    $lumifile=~ s/lumi_mask =/ /g;
	    system(sprintf("cp $lumifile $dir"));
	    system(sprintf("./subs \"<lumi_mask>\"              \"$lumi_mask[$idx] \"                $dir/crab.cfg"));
	    system(sprintf("./subs \"<total_number_of_lumis>\"  \"$total_number_of_lumis[$idx] \"    $dir/crab.cfg"));
	}
	system(sprintf("./subs \"<total_number_of_events>\" \"$total_number_of_events[$idx] \"       $dir/crab.cfg"));
	system(sprintf("./subs \"<number_of_jobs>\"         \"$number_of_jobs[$idx] \"               $dir/crab.cfg"));
	system(sprintf("./subs \"<number_of_jobs>\"         \"$number_of_jobs[$idx] \"               $dir/crab.cfg"));
	if($CE_white_list[$idx] ne "none" || $CE_white_list[$idx] ne ""){
	    system(sprintf("./subs \"<CE_white_list>\"          \"$CE_white_list[$idx] \"            $dir/crab.cfg"));
	}
	if($CE_black_list[$idx] ne "none" || $CE_black_list[$idx] ne ""){
            system(sprintf("./subs \"<CE_black_list>\"          \"$CE_black_list[$idx] \"            $dir/crab.cfg"));
        }
	if($njobs !=0){
	    system(sprintf("cd $dir ; crab -create -submit $njobs ; cd .."));
	}
	else{
	    system(sprintf("echo 'cd $dir ; crab -create ; crab -submit 1; cd ..' >>  createandsubmit_test \n"));
	    system(sprintf("echo 'cd $dir ;  crab -submit ; cd ..' >>  createandsubmit \n"));
	    system(sprintf("echo 'cd $dir; crab -getoutput; cd ..' >> getoutput \n"));
	}
    	$idx++;  
    }
    printf("The Submission Directories have been set up....\n");
    printf("To create and submit a test version of your crab jobs: source createandsubmit_test \n");
    printf("To create and submit the crab jobs: source createandsubmit \n");
    printf("To get the log files from the crab jobs: source getoutput \n");
    printf("NOTE: PLEASE VALIDATE YOUR CODE RUNS BEFORE SUBMITTING ALL JOBS (ie source createandsubmit_test)\n");

}



if( $ARGV[0] eq "--SkimSummary" ){
    $TempDataSetFile=$ARGV[1];
    $CodeDir=$ARGV[2];
    @ID;
    @NEvents;
    @NEventsErr;
    @NEvents_sel;
    @NEventsErr_sel;
    @NEvents_noweight;
    @NEvents_noweight_sel;
    @NFiles;

    @DataType;
    open(DAT, $TempDataSetFile) || die("Could not open file $TempDataSetFile! [ABORTING]");
    $idx=-1;
    while ($item = <DAT>) {
        chomp($item);
        ($a,$b,$c,$d)=split(/ /,$item);
        if($a eq "DataType"){
	    push(@DataType,$c);
	}
    }
    close(DAT);
    $idx=0;
    $diridx=0;
    foreach $data (@DataType){
	printf("Looking for: $data \n");
        $datadir=$data;
        $datadir=~ s/.root/_CRAB/g;
        $datadir=~ s/DataType =/ /g;
        $datadir.=sprintf("%d", $diridx);
	$diridx++;
	$idx++;
	$myDIR=getcwd;
	opendir(DIR,"$myDIR/$datadir/");
	printf("Searching: $myDIR/$datadir/ \n");
	system(sprintf("ls $myDIR/$datadir/"));
	@dirs = grep {(/crab_/)} readdir(DIR);
	closedir DIR;
	foreach $subdir (@dirs){
	    printf("Opening Dir: $myDIR/$datadir/$subdir\n");
	    opendir(SUBDIR,"$myDIR/$datadir/$subdir/res/");
	    @files = grep { /stdout/ } readdir(SUBDIR);
	    foreach $file (@files){
		open(INPUT,"$myDIR/$datadir/$subdir/res/$file")  || die "can't open log file $myDIR/$datadir/$subdir/res/$file" ;
		while (<INPUT>) {
		    ($i1,$i2,$i3,$i4,$i5,$i6,$i7,$i8,$i9,$i10,$i11,$i12,$i13)=split(/ /,$_);
		    if($i1 eq "[EventCounter-AllEvents]:" || $i1 eq "[EventCounter-BeforeTauNtuple]:"){
			$flag=0;
		      IDLOOP: {
			  foreach $currentid (@ID){
			      if($currentid eq $i2){
				  last IDLOOP;
			      }
			      $flag++;
			  }
		      }
			$size=@ID;
			if($flag==$size){
			    push(@ID,$i2);
			    push(@NEvents,0);
			    push(@NEventsErr,0);
			    push(@NEvents_sel,0);
			    push(@NEventsErr_sel,0);
			    push(@NEvents_noweight,0);
			    push(@NEvents_noweight_sel,0);
			    push(@NFiles,0);
			}
			if($i1 eq "[EventCounter-AllEvents]:"){
			    $NEvents[$flag]+=$i7;
			    $NEvents_noweight[$flag]+=$i13;
			    $tmp=$NEventsErr[$flag];
			    $NEventsErr[$flag]=sqrt($tmp*$tmp+$i9*$i9);
			    $NFiles[$flag]+=1;
			}
			if($i1 eq "[EventCounter-BeforeTauNtuple]:"){
			    $NEvents_sel[$flag]+=$i7;
			    $NEvents_noweight_sel[$flag]+=$i13;
			    $tmp=$NEventsErr_sel[$flag];
                            $NEventsErr_sel[$flag]=sqrt($tmp*$tmp+$i9*$i9);
			}
		    }
		}
		close(OUTPUT) ;
		$idx=0;
		system(sprintf("rm SkimSummary.log"));
		foreach $currentid (@ID){
		    system(sprintf("echo \"ID= %d AllEvt= %f AllEvtErr= %f SelEvt= %f  SelEvtErr= %f AllEvtnoweight= %f SelEvtnoweight= %f Eff(weight)= %f Eff(noweight)= %f Nfile= %d \" >> SkimSummary.log",$ID[$idx],$NEvents[$idx],$NEventsErr[$idx],$NEvents_sel[$idx],$NEventsErr_sel[$idx],$NEvents_noweight[$idx],$NEvents_noweight_sel[$idx], $NEvents_sel[$idx]/$NEvents[$idx],$NEvents_noweight_sel[$idx]/$NEvents_noweight[$idx],$NFiles[$idx]));
		    $idx++;
		}
	    }
	}
    }
    system(sprintf("cp SkimSummary.log $CodeDir/InputData/SkimSummary.log "));
    printf("SkimSummary.log has been generated. It has been copied to $CodeDir/InputData/SkimSummary.log\n ");
}



if( $ARGV[0] eq "--CheckandCleanOutput" ){
    $TempDataSetFile=$ARGV[1];
    @DataType;
    open(DAT, $TempDataSetFile) || die("Could not open file $TempDataSetFile! [ABORTING]");
    $idx=-1;
    while ($item = <DAT>) {
        chomp($item);
        ($a,$b,$c,$d)=split(/ /,$item);
        if($a eq "DataType"){
            push(@DataType,$c);
        }
    }
    close(DAT);


    foreach $data (@DataType){
        printf("Looking for: $data \n");
        $datadir=$data;
        $datadir=~ s/.root/_CRAB/g;
        $datadir=~ s/DataType =/ /g;
        $datadir.=sprintf("%d", $diridx);
        $diridx++;
        $idx++;
        $myDIR=getcwd;
        opendir(DIR,"$myDIR/$datadir/");
        printf("Searching: $myDIR/$datadir/ \n");
        system(sprintf("ls $myDIR/$datadir/"));
        @dirs = grep {(/crab_/)} readdir(DIR);
        closedir DIR;
        foreach $subdir (@dirs){
	    system(sprintf("rm  $myDIR/$datadir/OutputFilesfromDisk.log"));
	    system(sprintf("rm $myDIR/$datadir/OutputFilesfromlog.log"));
            system(sprintf("rm $myDIR/$datadir/DiffLogAndDisk.log"));
            system(sprintf("rm FileSummary.log"));
            printf("Opening Dir: $myDIR/$datadir/$subdir\n");
            opendir(SUBDIR,"$myDIR/$datadir/$subdir/res/");
            @files = grep { /stdout/ } readdir(SUBDIR);
	    system(sprintf("rm junk1; touch junk1"));
            foreach $file (@files){
		system(sprintf("grep \"LFN:\"  $myDIR/$datadir/$subdir/res/$file  | grep -v \"echo\"  >> junk1"));
	    }
	    system(sprintf("cat junk1 | awk '{ split(\$2,a,\"/TauNtuple\"); print \"TauNtuple\"a[2] }' | tee $myDIR/$datadir/OutputFilesfromlog.log"));
	    system(sprintf("tail -n 1 junk1 | awk '{ split(\$2,a,\"/TauNtuple\"); print \"uberftp grid-ftp.physik.rwth-aachen.de \\\"cd /pnfs/physik.rwth-aachen.de/cms\"  a[1]  \" ; ls */ \\\" | tee junk3 \"}' > junk2")); 
	    system(sprintf("echo \"grep root junk3 | awk '{print \\\$9 }'| tee $myDIR/$datadir/OutputFilesfromDisk.log   \" >> junk2"));
	    system(sprintf("source junk2;"));
	    system(sprintf("echo 'N Files found in in$myDIR/$datadir/OutputFilesfromlog.log: ' >> FileSummary.log "));
	    system(sprintf("cat $myDIR/$datadir/OutputFilesfromlog.log | wc -l >> FileSummary.log"));
	    system(sprintf("echo 'N Files found in in$myDIR/$datadir/OutputFilesfromDisk.log: ' >> FileSummary.log "));
	    system(sprintf("cat $myDIR/$datadir/OutputFilesfromDisk.log | wc -l >> FileSummary.log"));

	    @ListfromDisk=();
	    open(DAT, "$myDIR/$datadir/OutputFilesfromDisk.log") || die("Could not open file $myDIR/$datadir/OutputFilesfromDisk.log! [ABORTING]");
	    $idx=-1;
	    while ($item = <DAT>) {
		chomp($item);
		push(@ListfromDisk,$item);
	    }
	    close(DAT);

	    @ListfromLog=();
	    open(DAT, "$myDIR/$datadir/OutputFilesfromlog.log") || die("Could not open file $myDIR/$datadir/OutputFilesfromlog.log! [ABORTING]");
	    $idx=-1;
	    while ($item = <DAT>) {
		chomp($item);
		push(@ListfromLog,$item);
	    }
	    close(DAT);
	   
 
	    foreach $thedisk (@ListfromDisk){
		$match=0;
		foreach $thelog (@ListfromLog){
		    if($thedisk eq $thelog){
			printf("match");
			$match=1;
		    }
		}
		printf("$thedisk $match\n"); 
		if($match != 1){
		    system(sprintf("echo '$thedisk' >> $myDIR/$datadir/DiffLogAndDisk.log "));
		}
	    }

            system(sprintf("rm junk1; touch junk1"));
            system(sprintf("rm junk2; touch junk2"));
            system(sprintf("rm junk3; touch junk3"));
            system(sprintf("rm junk4; touch junk4"));

	}
    }
}
