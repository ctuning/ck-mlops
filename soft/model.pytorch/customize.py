#
# Collective Knowledge (individual environment - setup)
#
# See CK LICENSE.txt for licensing details
# See CK COPYRIGHT.txt for copyright details
#
# Developer: Grigori Fursin, Grigori.Fursin@cTuning.org, http://fursin.net
#

import os

##############################################################################
# setup environment setup

def setup(i):
    """
    Input:  {
              cfg              - meta of this soft entry
              self_cfg         - meta of module soft
              ck_kernel        - import CK kernel module (to reuse functions)

              host_os_uoa      - host OS UOA
              host_os_uid      - host OS UID
              host_os_dict     - host OS meta

              target_os_uoa    - target OS UOA
              target_os_uid    - target OS UID
              target_os_dict   - target OS meta

              target_device_id - target device ID (if via ADB)

              tags             - list of tags used to search this entry

              env              - updated environment vars from meta
              customize        - updated customize vars from meta

              deps             - resolved dependencies for this soft

              interactive      - if 'yes', can ask questions, otherwise quiet
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              bat          - prepared string for bat file
            }

    """

    import os

    # Get variables
    ck=i['ck_kernel']
    s=''

    iv=i.get('interactive','')

    cus=i.get('customize',{})
    fp=cus.get('full_path','')

    env=i['env']

    hosd=i['host_os_dict']
    tosd=i['target_os_dict']

    sdirs=hosd.get('dir_sep','')

    # Check platform
    hplat=hosd.get('ck_name','')

    hproc=hosd.get('processor','')
    tproc=tosd.get('processor','')

    remote=tosd.get('remote','')
    tbits=tosd.get('bits','')

    pi=os.path.dirname(fp)

    ep=cus['env_prefix']
    env[ep]=pi

    x=cus.get('file_model','')
    if x!='': 
       env[ep+'_PT_NAME']=x
       env[ep+'_PT']=pi+sdirs+x

    x=cus.get('file_model_pttxt','')
    if x!='': 
       env[ep+'_PTTXT_NAME']=x
       env[ep+'_PTTXT']=pi+sdirs+x

    x=cus.get('file_labels','')
    if x!='': 
       env[ep+'_LABELS_NAME']=x
       env[ep+'_LABELS']=pi+sdirs+x

    # Call common script
    r=ck.access({'action':'run', 'module_uoa':'script', 'data_uoa':'process-model', 
                 'code':'common_vars', 'func':'process', 
                 'dict':i})
    if r['return']>0: return r

    env.update(r['env'])

    return {'return':0, 'bat':s}
