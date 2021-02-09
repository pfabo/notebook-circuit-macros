import os
import sys
import random

cm_template='''
.PS
pi=3.14159265359
                        # parametre z PIC (resp. GNU PIC)
scale = 2.54            # cm - jednotka pre obrazok
maxpswid = 30           # rozmery obrazku
maxpsht = 30            # 30 x 30cm, default je 8.5x11 inch
cct_init                # inicializacia lokalnych premennych

arrowwid  = 0.127       # parametre sipok - sirka
arrowht = 0.254         # dlzka
include(user.ckt)       # externa kniznica
#-----------------------------------------------------------------------
Origin: Here 
size_x = 10
size_y = 6
d = 2;                  # 1cm zakladna dlzka

# mriezka
move to (-0.5, size_y/2); grid(size_x, size_y); move to 0,0;
#=======================================================================

.PE
'''


# template pre zahlavie suboru, predpoklada sa pouzitie z notebooku,
# ktory je v nadradenom adresari (cesta k user.ckt)
cm_start = '''
.PS
pi=3.14159265359
                        # parametre z PIC (resp. GNU PIC)
scale = 2.54            # cm - jednotka pre obrazok
maxpswid = 30           # rozmery obrazku
maxpsht = 30            # 30 x 30cm, default je 8.5x11 inch
cct_init                # inicializacia lokalnych premennych

arrowwid  = 0.127       # parametre sipok - sirka
arrowht = 0.254         # dlzka
include(./img/user.ckt)       # externa kniznica
#-----------------------------------------------------------------------
Origin: Here 
size_x = 10
size_y = 6
d = 2;                  # 1cm zakladna dlzka

# mriezka
move to (-0.5, size_y/2); grid(size_x, size_y); move to 0,0;
#=======================================================================
# uzivatelske data - zaciatok
#=======================================================================
'''

# teplate pre koniec suboru
cm_end = '''
#=======================================================================
# uzivatelske data - koniec
#=======================================================================
.PE
'''


#------------------------------------------------------------------------



def cm_show(file_name, cm_data='', width=400):
    '''
    Zobrazenie obr8zku v jupiter notebooku
    '''
    fp = open('./img/' + file_name + '.ckt', 'w'); 
    fp.write(cm_start + cm_data + cm_end); 
    fp.close()

    cm2ps('./img/' + file_name + '.ckt' ); 
    show_png('./img/' + file_name + '.png', width)




def create_cm(file_name, overwrite='No'):
    if os.path.isfile(file_name) and overwrite=='No': 
        return 'File exists, has not been overwritten ...'
    else:
        fp = open(file_name, 'w')
        fp.write(cm_template)
        fp.close
        return 'A new file has been created ...'


CIRCUIT_MACROS_PATH = './img/cm'


def cm2ps(fname):
    '''
    Konverzia cm na eps
    '''

    fname_base = os.path.splitext(fname )[0]
    texfile      = fname_base + '_pst'
    templatefile = fname_base + '.tex'
    epsfile      = fname_base + '.eps'

    #print('>> m4 pstricks')
    os.system( 'm4 -I %s pstricks.m4 %s | dpic -p > %s'%(CIRCUIT_MACROS_PATH, fname, texfile+'.tex') )

    latextemplate = '''\\documentclass{article}
    \\usepackage{times,pstricks,pst-eps,pst-grad,xfrac}
    \\usepackage{graphicx}
    \\begin{document}
    \\begin{TeXtoEPS}
    \\input %s
    \\end{TeXtoEPS}\\end{document}
    '''%texfile

    f = open( templatefile, 'w' )
    f.write( latextemplate )
    f.flush()
    f.close()

    #print('>> latex')    
    os.system( 'latex -output-directory=./img/  %s'%templatefile )       

    #print('>> dvips')
    os.system( 'dvips  -E %s -o %s '%(fname_base, epsfile) ) 
    
    # na poradi argumentov ZALEZI !!!
    #print('>> convert eps to png')
    os.system('convert -density 600 -quality 100 -flatten %s -colorspace RGB %s'%(epsfile, fname_base+'.png'))

    #os.system( 'dvips -Ppdf -G0 -E %s -o %s'%(fname_base, epsfile) )
    #os.system( 'rm '+fname_base + '.dvi' ) 
    #os.system( 'rm '+fname_base + '.aux' ) 
    #os.system( 'rm '+fname_base + '.log' ) 
        

def show_png(pngfile, width=300):
    '''
    Zrusenie image-cache pri zobrazeni obrazku v html stranke notebooku
    '''
    counter=random.randint(0,2e9)
    # now use IPython's rich display to display the html image with the
    # new argument
    from IPython.display import HTML, display
    display(HTML('<img src="%s?%d" alt="Obrazok %s" width=%d>' %(pngfile, counter, pngfile, width) ) )
    
        
