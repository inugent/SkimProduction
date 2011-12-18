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
    printf("    data\n");
    printf("    h_tautau\n");
    printf("    hpm_taunu\n");
    printf("    ttbar\n");
    printf("    w_lnu\n");
    printf("    w_enu\n");
    printf("    w_munu\n");
    printf("    w_taunu\n");
    printf("    dy_ll\n");
    printf("    dy_ee\n");
    printf("    dy_mumu\n");
    printf("    dy_tautau\n");
    printf("    ZZ\n");
    printf("    WW\n");
    printf("    WZ\n");
    printf("    qcd\n");
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
	printf("\ncreating dir: $dir\n");
	system(sprintf("mkdir $dir; cp crab_TEMPLATE.cfg  $dir/crab.cfg;cp $pythonfile $dir/"));
	system(sprintf("./subs \"<DataType>\"               \"$DataType[$idx]\"                      $dir/$pythonfile"));
	system(sprintf("./subs \"<globaltag>\"               \"$globaltag[$idx]\"                    $dir/$pythonfile"));
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
    	$idx++;  
    }
}
