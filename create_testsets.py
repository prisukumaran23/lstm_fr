#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import os
import pandas as pd

# create phrases for simple gender agreement without attractors
def create_tests_a(test_cond,test_target,path_paradigms,path_nounlist,path_adjlist):   
    paradigms = pd.DataFrame()
    nouns = pd.DataFrame()
    adjs = pd.DataFrame()
        
    paradigms = pd.read_csv(path_paradigms)  
    nouns = pd.read_csv(path_nounlist)  
    adjs = pd.read_csv(path_adjlist) 
    for i_p,p in paradigms.iterrows(): 
        sents = pd.DataFrame(columns=('Paradigm','Gen', 'Num', 'Sent', 'Eval', 'Corr', 'Wrong', 'Dist'))
        paradigm = p[0]
        art = str()
        if p['Number'] == 'P':
            adjs_use = adjs.loc[adjs['Number'].isin(['P'])] # select only plural adjectives
            nouns_use = nouns.loc[nouns['Number'].isin(['P'])] # select only plural nouns
        elif p['Number'] == 'S':
            adjs_use = adjs.loc[adjs['Number'].isin(['S'])] # select only single adjectives
            nouns_use = nouns.loc[nouns['Number'].isin(['S'])] # select only single nouns
        for i_n,n in nouns_use.iterrows():
            adjs_use_F = adjs_use.loc[adjs_use['Gender'].isin(['F'])] # select only feminine adjectives
            adjs_use_M = adjs_use.loc[adjs_use['Gender'].isin(['M'])] # select only masculine adjectives
            if p['Number'] == 'S' and n['Gender'] == 'F': 
                art = 'la'
                adjs_use_final = adjs_use_F
            elif p['Number'] == 'S' and n['Gender'] == 'M': 
                art = 'le'
                adjs_use_final = adjs_use_M
            elif p['Number'] == 'P' and n['Gender'] == 'F':  
                art = 'les' 
                adjs_use_final = adjs_use_F
            elif p['Number'] == 'P' and n['Gender'] == 'M': 
                art = 'les' 
                adjs_use_final = adjs_use_M
            for i_a,a in adjs_use_final.iterrows():
                if pd.isna(p['Clause']):
                    sent = art+' '+n['Noun']+' '+a[test_target]+' <eos>'
                else: 
                    sent = art+' '+n['Noun']+' '+p['Clause']+' '+a[test_target]+' <eos>'
                sents = sents.append(pd.DataFrame({'Paradigm':paradigm,'Gen':n['Gender'],'Num':n['Number'],'Sent':sent,
                                                  'Eval':p['Eval'],'Corr':a[test_target],'Wrong':a['Gender_Alt'],'Dist':p['Dist']},index=[(i_p,i_n,i_a)]))
        cond_directory = 'testsets/testsets_'+test_cond+'/'
        if not os.path.exists(cond_directory):
            os.makedirs(cond_directory)
        directory = cond_directory+paradigm
        if not os.path.exists(directory):
            os.makedirs(directory)
        print(paradigm, "done")
        np.savetxt('testsets/testsets_'+test_cond+'/'+paradigm+'/'+paradigm+'.gold', sents[['Eval','Corr','Wrong','Dist']], fmt='%s',delimiter='\t')
        np.savetxt('testsets/testsets_'+test_cond+'/'+paradigm+'/'+paradigm+'.eval', sents[['Eval']], fmt='%d',delimiter='\t')
        np.savetxt('testsets/testsets_'+test_cond+'/'+paradigm+'/'+paradigm+'.text', sents[['Sent']], fmt='%s',delimiter='\t')
        np.savetxt('testsets/testsets_'+test_cond+'/'+paradigm+'/'+paradigm+'.info', sents, fmt='%s',delimiter='\t')
        
# create phrases with an attractor of opposite gender
def create_tests_b(test_cond,test_target,path_paradigms,path_nounlist,path_adjlist):   
    test_dir = 'testsets/'

    paradigms = pd.DataFrame()
    nouns = pd.DataFrame()
    adjs = pd.DataFrame()
        
    paradigms = pd.read_csv(path_paradigms)  
    nouns = pd.read_csv(path_nounlist)  
    adjs = pd.read_csv(path_adjlist) 
    
    for i_p,p in paradigms.iterrows(): 
        sents = pd.DataFrame(columns=('Paradigm','Gen', 'Num', 'Sent', 'Eval', 'Corr', 'Wrong', 'Dist', 'Attr_Gen'))
        paradigm = p[0]
        if p['Number'] == 'P':
            adjs_use = adjs.loc[adjs['Number'].isin(['P'])]    # select only plural adjectives
            nouns_use = nouns.loc[nouns['Number'].isin(['P'])] # select only plural nouns
        elif p['Number'] == 'S':
            adjs_use = adjs.loc[adjs['Number'].isin(['S'])]    # select only single adjectives
            nouns_use = nouns.loc[nouns['Number'].isin(['S'])] # select only single nouns
        for i_n,n in nouns_use.iterrows():
            adjs_use_F = adjs_use.loc[adjs_use['Gender'].isin(['F'])] # select only feminine adjectives
            adjs_use_M = adjs_use.loc[adjs_use['Gender'].isin(['M'])] # select only masculine adjectives
            if n['Gender'] == 'F': 
                adjs_use_final = adjs_use_F
            elif n['Gender'] == 'M': 
                adjs_use_final = adjs_use_M
            # remove current noun to create list of attractors nouns
            nouns_attr = nouns_use.drop(nouns_use[nouns_use.Noun == n['Noun']].index)
            for i_na,na in nouns_attr.iterrows():
                for i_a,a in adjs_use_final.iterrows():
                        sent = n['Article']+' '+n['Noun']+' avec '+na['Article']+' '+na['Noun']+' '+p['Clause']+' '+a[test_target]+' <eos>'
                        sents = sents.append(pd.DataFrame({'Paradigm':paradigm,'Gen':n['Gender'],'Num':n['Number'],'Sent':sent,
                                                      'Eval':p['Eval'],'Corr':a[test_target],'Wrong':a['Gender_Alt'],'Dist':p['Dist'], 'Attr_Gen':na['Gender']},index=[(i_p,i_n,i_a)]))
        print(paradigm, "done")
        if p['Number'] == 'S':
            sents_si_opp = sents.loc[sents['Gen']!=sents['Attr_Gen']]
            sents_si_same = sents.loc[sents['Gen']==sents['Attr_Gen']]
            directory = test_dir+'testsets_'+test_cond+'/single_opp/'+paradigm
            if not os.path.exists(directory):
                os.makedirs(directory)
            directory = test_dir+'testsets_'+test_cond+'/single_same/'+paradigm
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            np.savetxt(test_dir+'testsets_'+test_cond+'/single_opp/'+paradigm+'/'+paradigm+'.gold', sents_si_opp[['Eval','Corr','Wrong','Dist']], fmt='%s',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/single_opp/'+paradigm+'/'+paradigm+'.eval', sents_si_opp[['Eval']], fmt='%d',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/single_opp/'+paradigm+'/'+paradigm+'.info', sents_si_opp, fmt='%s',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/single_opp/'+paradigm+'/'+paradigm+'.text', sents_si_opp[['Sent']], fmt='%s',delimiter='\t')
            
            np.savetxt(test_dir+'testsets_'+test_cond+'/single_same/'+paradigm+'/'+paradigm+'.gold', sents_si_same[['Eval','Corr','Wrong','Dist']], fmt='%s',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/single_same/'+paradigm+'/'+paradigm+'.eval', sents_si_same[['Eval']], fmt='%d',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/single_same/'+paradigm+'/'+paradigm+'.info', sents_si_same, fmt='%s',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/single_same/'+paradigm+'/'+paradigm+'.text', sents_si_same[['Sent']], fmt='%s',delimiter='\t')
            print(paradigm, "saved")
            
        elif p['Number'] == 'P':
            sents_pl_opp = sents.loc[sents['Gen']!=sents['Attr_Gen']]
            sents_pl_same = sents.loc[sents['Gen']==sents['Attr_Gen']]
            directory = test_dir+'testsets_'+test_cond+'/plural_opp/'+paradigm
            if not os.path.exists(directory):
                os.makedirs(directory)
            directory = test_dir+'testsets_'+test_cond+'/plural_same/'+paradigm
            if not os.path.exists(directory):
                os.makedirs(directory)
    
            np.savetxt(test_dir+'testsets_'+test_cond+'/plural_opp/'+paradigm+'/'+paradigm+'.gold', sents_pl_opp[['Eval','Corr','Wrong','Dist']], fmt='%s',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/plural_opp/'+paradigm+'/'+paradigm+'.eval', sents_pl_opp[['Eval']], fmt='%d',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/plural_opp/'+paradigm+'/'+paradigm+'.info', sents_pl_opp, fmt='%s',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/plural_opp/'+paradigm+'/'+paradigm+'.text', sents_pl_opp[['Sent']], fmt='%s',delimiter='\t')
            
            np.savetxt(test_dir+'testsets_'+test_cond+'/plural_same/'+paradigm+'/'+paradigm+'.gold', sents_pl_same[['Eval','Corr','Wrong','Dist']], fmt='%s',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/plural_same/'+paradigm+'/'+paradigm+'.eval', sents_pl_same[['Eval']], fmt='%d',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/plural_same/'+paradigm+'/'+paradigm+'.info', sents_pl_same, fmt='%s',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/plural_same/'+paradigm+'/'+paradigm+'.text', sents_pl_same[['Sent']], fmt='%s',delimiter='\t')
            print(paradigm, "saved")
    
# create phrases with an attractor of opposite gender and number
def create_tests_c(test_cond,test_target,path_paradigms,path_nounlist,path_adjlist):  
    test_dir = 'testsets/'
    
    paradigms = pd.DataFrame()
    nouns = pd.DataFrame()
    adjs = pd.DataFrame()
        
    paradigms = pd.read_csv(path_paradigms)  
    nouns = pd.read_csv(path_nounlist)  
    adjs = pd.read_csv(path_adjlist) 
    
    for i_p,p in paradigms.iterrows(): 
        sents = pd.DataFrame(columns=('Paradigm','Gen', 'Num', 'Sent', 'Eval', 'Corr', 'Wrong', 'Dist','Attr_Gen','Attr_Num'))
        paradigm = p[0]
        if p['Number'] == 'P':
            adjs_use = adjs.loc[adjs['Number'].isin(['P'])]    # select only plural adjectives
            nouns_use = nouns.loc[nouns['Number'].isin(['P'])] # select only plural nouns
            nouns_attr = nouns.loc[nouns['Number'].isin(['S'])] # select only plural nouns
        elif p['Number'] == 'S':
            adjs_use = adjs.loc[adjs['Number'].isin(['S'])]    # select only single adjectives
            nouns_use = nouns.loc[nouns['Number'].isin(['S'])] # select only single nouns
            nouns_attr = nouns.loc[nouns['Number'].isin(['P'])] # select only plural nouns
        for i_n,n in nouns_use.iterrows():
            adjs_use_F = adjs_use.loc[adjs_use['Gender'].isin(['F'])] # select only feminine adjectives
            adjs_use_M = adjs_use.loc[adjs_use['Gender'].isin(['M'])] # select only masculine adjectives
            if n['Gender'] == 'F': 
                adjs_use_final = adjs_use_F
            elif n['Gender'] == 'M': 
                adjs_use_final = adjs_use_M
            for i_na,na in nouns_attr.iterrows():
                for i_a,a in adjs_use_final.iterrows():
                        sent = n['Article']+' '+n['Noun']+' avec '+na['Article']+' '+na['Noun']+' '+p['Clause']+' '+a[test_target]+' <eos>'
                        sents = sents.append(pd.DataFrame({'Paradigm':paradigm,'Gen':n['Gender'],'Num':n['Number'],'Sent':sent,
                                                      'Eval':p['Eval'],'Corr':a[test_target],'Wrong':a['Gender_Alt'],'Dist':p['Dist'], 'Attr_Gen':na['Gender'], 'Attr_Num':na['Number']},index=[(i_p,i_n,i_a)]))
        print(paradigm, "done")
        if p['Number'] == 'S':
            sents_si_opp = sents.loc[sents['Gen']!=sents['Attr_Gen']]
            sents_si_same = sents.loc[sents['Gen']==sents['Attr_Gen']]
            directory = test_dir+'testsets_'+test_cond+'/single_opp/'+paradigm
            if not os.path.exists(directory):
                os.makedirs(directory)
            directory = test_dir+'testsets_'+test_cond+'/single_same/'+paradigm
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            np.savetxt(test_dir+'testsets_'+test_cond+'/single_opp/'+paradigm+'/'+paradigm+'.gold', sents_si_opp[['Eval','Corr','Wrong','Dist']], fmt='%s',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/single_opp/'+paradigm+'/'+paradigm+'.eval', sents_si_opp[['Eval']], fmt='%d',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/single_opp/'+paradigm+'/'+paradigm+'.info', sents_si_opp, fmt='%s',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/single_opp/'+paradigm+'/'+paradigm+'.text', sents_si_opp[['Sent']], fmt='%s',delimiter='\t')
            
            np.savetxt(test_dir+'testsets_'+test_cond+'/single_same/'+paradigm+'/'+paradigm+'.gold', sents_si_same[['Eval','Corr','Wrong','Dist']], fmt='%s',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/single_same/'+paradigm+'/'+paradigm+'.eval', sents_si_same[['Eval']], fmt='%d',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/single_same/'+paradigm+'/'+paradigm+'.info', sents_si_same, fmt='%s',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/single_same/'+paradigm+'/'+paradigm+'.text', sents_si_same[['Sent']], fmt='%s',delimiter='\t')
            print(paradigm, "saved")
            
        elif p['Number'] == 'P':
            sents_pl_opp = sents.loc[sents['Gen']!=sents['Attr_Gen']]
            sents_pl_same = sents.loc[sents['Gen']==sents['Attr_Gen']]
            directory = test_dir+'testsets_'+test_cond+'/plural_opp/'+paradigm
            if not os.path.exists(directory):
                os.makedirs(directory)
            directory = test_dir+'testsets_'+test_cond+'/plural_same/'+paradigm
            if not os.path.exists(directory):
                os.makedirs(directory)
    
            np.savetxt(test_dir+'testsets_'+test_cond+'/plural_opp/'+paradigm+'/'+paradigm+'.gold', sents_pl_opp[['Eval','Corr','Wrong','Dist']], fmt='%s',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/plural_opp/'+paradigm+'/'+paradigm+'.eval', sents_pl_opp[['Eval']], fmt='%d',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/plural_opp/'+paradigm+'/'+paradigm+'.info', sents_pl_opp, fmt='%s',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/plural_opp/'+paradigm+'/'+paradigm+'.text', sents_pl_opp[['Sent']], fmt='%s',delimiter='\t')
            
            np.savetxt(test_dir+'testsets_'+test_cond+'/plural_same/'+paradigm+'/'+paradigm+'.gold', sents_pl_same[['Eval','Corr','Wrong','Dist']], fmt='%s',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/plural_same/'+paradigm+'/'+paradigm+'.eval', sents_pl_same[['Eval']], fmt='%d',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/plural_same/'+paradigm+'/'+paradigm+'.info', sents_pl_same, fmt='%s',delimiter='\t')
            np.savetxt(test_dir+'testsets_'+test_cond+'/plural_same/'+paradigm+'/'+paradigm+'.text', sents_pl_same[['Sent']], fmt='%s',delimiter='\t')
            print(paradigm, "saved")

test_cond = 'noun_pass'
test_target = 'Verb'
path_paradigms = 'utils_create/'+test_cond+'/paradigms.csv'
path_nounlist = 'utils_create/'+test_cond+'/nounlist.csv'
path_adjlist = 'utils_create/'+test_cond+'/verbpassivelist.csv'

create_tests_a(test_cond,test_target,path_paradigms,path_nounlist,path_adjlist)

test_cond = 'noun_adj'
test_target = 'Adj'
path_paradigms = 'utils_create/'+test_cond+'/paradigms.csv'
path_nounlist = 'utils_create/'+test_cond+'/nounlist.csv'
path_adjlist = 'utils_create/'+test_cond+'/adjlist.csv'

create_tests_a(test_cond,test_target,path_paradigms,path_nounlist,path_adjlist)

test_cond = 'noun_pass_noun_same'
test_target = 'Verb'
path_paradigms = 'utils_create/'+test_cond+'/paradigms.csv'
path_nounlist = 'utils_create/'+test_cond+'/nounlist.csv'
path_adjlist = 'utils_create/'+test_cond+'/verbpassivelist.csv'

create_tests_b(test_cond,test_target,path_paradigms,path_nounlist,path_adjlist)

test_cond = 'noun_adj_noun_same'
test_target = 'Adj'
path_paradigms = 'utils_create/'+test_cond+'/paradigms.csv'
path_nounlist = 'utils_create/'+test_cond+'/nounlist.csv'
path_adjlist = 'utils_create/'+test_cond+'/adjlist.csv'

create_tests_b(test_cond,test_target,path_paradigms,path_nounlist,path_adjlist)

test_cond = 'noun_pass_noun_opp'
test_target = 'Verb'
path_paradigms = 'utils_create/'+test_cond+'/paradigms.csv'
path_nounlist = 'utils_create/'+test_cond+'/nounlist.csv'
path_adjlist = 'utils_create/'+test_cond+'/verbpassivelist.csv'

create_tests_c(test_cond,test_target,path_paradigms,path_nounlist,path_adjlist)

test_cond = 'noun_adj_noun_opp'
test_target = 'Adj'
path_paradigms = 'utils_create/'+test_cond+'/paradigms.csv'
path_nounlist = 'utils_create/'+test_cond+'/nounlist.csv'
path_adjlist = 'utils_create/'+test_cond+'/adjlist.csv'

create_tests_c(test_cond,test_target,path_paradigms,path_nounlist,path_adjlist)

