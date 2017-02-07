'''
* Created by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* License: this code is in GPL license
* Last modified: 2017-02-07
'''

if __name__ == '__main__':
    print('-> you run ', __file__, ' file in a main mode')
    print('----- SYS.ARGV{}:')
    print(sys.argv)
    if len(sys.argv) > 1:
        if sys.argv[1] == 'debug':
            print('-- script run in debug mode:')
            if len(sys.argv) > 2:
                path = r'/home/yugin/VirtualboxShare/Co-CoO/debug/out_genetic_CoO_no_Au'
                startCalculation(projPath=path, case_mix_or_layers=sys.argv[2])
        else:
            startCalculation(case_mix_or_layers=sys.argv[1])
    else:
        print('Can not run')
        print(sys.argv)