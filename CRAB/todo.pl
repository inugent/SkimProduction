#! /usr/bin/perl
use Cwd;
use POSIX;
#############################################
$numArgs = $#ARGV +1;
$ARGV[$argnum];

if($ARGV[0] eq "--help" || $ARGV[0] eq ""){
    printf("\nThis code requires one input option. The systax is:./todo.pl [OPTION]");
    printf("\nPlease choose from the following options:");
    printf("\n./todo.pl --help                                   Prints this message");
    printf("\n./todo.pl --Submit <python_cfg> <InputPar.txt>     Submit crab jobs to the grid");
    printf("\n                                                   <InputPar.txt> contains input command template.");
    printf("\n                                                   Option: --n number of jobs to submit [njobs=0 by default].");
    printf("\n                                                   PLEASE: run a test with --n 1 before production.");
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
    open(DAT, $TempDataSetFile) || die("Could not open file $TempDataSetFile! [ABORTING]");
    while ($item = <DAT>) {
	chomp($item);
	($b,$c,$d,$e,$f,$g,$h,$i,$j)=split(/ /,$item);
	if($b ne ""){
	    push(@datasetpath,$b);
	    push(@dbs_url,$c);
	    push(@publish_data_name,$d);
	    push(@output_file,$e);
	    push(@lumi_mask,$f);
	    push(@total_number_of_lumis,$g);
	    push(@total_number_of_events,$h);
	    push(@number_of_jobs,$i);
	    push(@CE_white_list,$j);
	    print("Read in Info: [$b] [$c] [$d] [$e] [$f] [$g] [$h] [$i] [$j]\n");
	}
    }
    close(DAT);

    ## create crab files and submit 
    $idx=0;
    foreach $data (@datasetpath){
	$dir=$output_file[$idx];
	$dir=~ s/.root/_CRAB/g;
	system(sprintf("mkdir $dir; cp crab_TEMPLATE.cfg  $dir/crab.cfg"));
	system(sprintf("./subs \"<datasetpath>\"            \"datasetpath = $datasetpath[$idx] \"                        $dir/crab.cfg"));
	system(sprintf("./subs \"<dbs_url>\"                \"dbs_url = $dbs_url[$idx] \"                                $dir/crab.cfg"));
	system(sprintf("./subs \"<publish_data_name>\"      \"publish_data_name = $publish_data_name[$idx] \"            $dir/crab.cfg"));
	system(sprintf("./subs \"<output_file>\"            \"output_file = $output_file[$idx] \"                        $dir/crab.cfg"));
	if($lumi_mask[$idx] ne "none"){
	    system(sprintf("cp $lumi_mask[$idx] $dir"));
	    system(sprintf("./subs \"<lumi_mask>\"              \"lumi_mask = $lumi_mask[$idx] \"                            $dir/crab.cfg"));
	    system(sprintf("./subs \"<total_number_of_lumis>\"  \"total_number_of_lumis = $total_number_of_lumis[$idx] \"    $dir/crab.cfg"));
	}
	system(sprintf("./subs \"<total_number_of_events>\" \"total_number_of_events = $total_number_of_events[$idx] \"  $dir/crab.cfg"));
	system(sprintf("./subs \"<number_of_jobs>\"         \"number_of_jobs = $number_of_jobs[$idx] \"                  $dir/crab.cfg"));
	system(sprintf("./subs \"<number_of_jobs>\"         \"number_of_jobs = $number_of_jobs[$idx] \"                  $dir/crab.cfg"));
	if($CE_white_list[$idx] ne "none" || $CE_white_list[$idx] ne ""){
	    system(sprintf("./subs \"<CE_white_list>\"          \"CE_white_list = $CE_white_list[$idx] \"                    $dir/crab.cfg"));
	}
	if($njobs !=0){
	    system(sprintf("cd $dir ; crab -create -submit $njobs ; cd .."));
	}
    	$idx++;  
    }
}
