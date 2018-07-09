from libsubmit.channels import SSHChannel
from libsubmit.providers import SlurmProvider

from parsl.config import Config
from parsl.executors.ipp import IPyParallelExecutor
from parsl.executors.threads import ThreadPoolExecutor


config = Config(
    executors=[
        IPyParallelExecutor(
            label='midway',
            provider=SlurmProvider(
                'westmere',
                channel=SSHChannel(
                    hostname='swift.rcc.uchicago.edu',
                    username='annawoodard',
                    script_dir='/scratch/midway2/annawoodard/parsl_scripts',
                ),
                init_blocks=1,
                min_blocks=1,
                max_blocks=1000,
                nodes_per_block=1,
                tasks_per_node=2,
                overrides='module load singularity; module load Anaconda3/5.1.0; source activate parsl_py36'
            ),
        ),
       ThreadPoolExecutor(label='local', max_threads=2)
    ],
)
