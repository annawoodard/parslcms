#!/bin/sh --noprofile

exit_on_error() {
    result=$1
    code=$2
    message=$3

    if [ $1 != 0 ]; then
        echo $3
        exit $2
    fi
}

log() {
    if [ $# -gt 2 ]; then
        short=$1
        long=$2
        shift; shift
        echo "==== $long @ $(date) ===="
        eval $*|while read line; do
            echo "== $short: $line"
        done
    else
        echo "=== $1 @ $(date)"
    fi
}

date +%s > t_wrapper_start

log "startup" "wrapper started" "echo -e 'hostname: $(hostname)\nkernel: $(uname -a)'"

log "env" "environment at startup" env
log "cpu" "cpu info" cat /proc/cpuinfo

log "os" "os release" cat /etc/redhat-release

log "sourcing CMS setup"
source /cvmfs/cms.cern.ch/cmsset_default.sh || exit_on_error $? 175 "Failed to source CMS"

slc=$(egrep "Red Hat Enterprise|Scientific|CentOS" /etc/redhat-release | sed 's/.*[rR]elease \([0-9]*\).*/\1/')
cmssw=$(echo $VC3_ROOT/sandbox-*tar.bz2 | grep -oe "CMSSW_[^-]*")
arch=$(echo $VC3_ROOT/sandbox-${cmssw}-slc${slc}*.tar.bz2 | grep -oe "slc${slc}_[^.-]*")
release_top="$VC3_ROOT/$cmssw"

log "env" "environment after sourcing startup scripts" env
log "dir" "working directory at startup" ls -l

export SCRAM_ARCH=$arch
if [ ! -d "$release_top" ]; then
  cd "$VC3_ROOT"
  scramv1 project -f CMSSW $cmssw || exit_on_error $? 173 "Failed to create new release"

  tar xjf $VC3_ROOT/sandbox-${cmssw}-${arch}-*.tar.bz2 || exit_on_error $? 170 "Failed to unpack sandbox!"
  cd -
fi

basedir=$PWD
cd $release_top
eval $(scramv1 runtime -sh) || exit_on_error $? 174 "The command 'cmsenv' failed!"
cd "$basedir"

log "top" "machine load" top -Mb\|head -n 50
log "env" "environment before execution" env
log "wrapper ready"
date +%s > t_wrapper_ready

log "dir" "working directory before execution" ls -l

$*
res=$?

log "dir" "working directory after execution" ls -l

log "wrapper done"
log "final return status = $res"

exit $res
