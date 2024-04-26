#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys,subprocess
import urllib
# python3
#import urllib.request, urllib.error
import re

from datetime import datetime

from sys import argv
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kWarning # remove info like : Info in <TCanvas::Print>: gif file gifs/h_ele_vertexPhi.gif has been created
argv.remove( '-b-' )

from ROOT import TCanvas, gStyle, gPad
from math import log10

import shutil
from configFunctions import read_config, check_schema_config


def getHisto(file, path):
    t_path = file.Get(path)
    print('t_path= ',t_path)
    return t_path

def RenderHisto(histo, canvas):

    if ("ELE_LOGY" in histo.GetOption() and histo.GetMaximum() > 0):
        canvas.SetLogy(1)
    histo_name_flag = 1 ; # use 0 to switch off
    if ( histo.InheritsFrom("TH2") ):
        gStyle.SetPalette(1)
        gStyle.SetOptStat(110+histo_name_flag)
    elif ( histo.InheritsFrom("TProfile") ):
        gStyle.SetOptStat(110+histo_name_flag)
    else: # TH1
        gStyle.SetOptStat(111110+histo_name_flag)

def initRootStyle():
    eleStyle = ROOT.TStyle("eleStyle","Style for electron validation")
    eleStyle.SetCanvasBorderMode(0)
    eleStyle.SetCanvasColor(ROOT.kWhite)
    eleStyle.SetCanvasDefH(600)
    eleStyle.SetCanvasDefW(800)
    eleStyle.SetCanvasDefX(0)
    eleStyle.SetCanvasDefY(0)
    eleStyle.SetPadBorderMode(0)
    eleStyle.SetPadColor(ROOT.kWhite)
    eleStyle.SetPadGridX(False)
    eleStyle.SetPadGridY(False)
    eleStyle.SetGridColor(0)
    eleStyle.SetGridStyle(3)
    eleStyle.SetGridWidth(1)
    eleStyle.SetOptStat(1)
    eleStyle.SetPadTickX(1)
    eleStyle.SetPadTickY(1)
    eleStyle.SetHistLineColor(1)
    eleStyle.SetHistLineStyle(0)
    eleStyle.SetHistLineWidth(2)
    eleStyle.SetEndErrorSize(2)
    eleStyle.SetErrorX(0.)
    eleStyle.SetTitleColor(1, "XYZ")
    eleStyle.SetTitleFont(42, "XYZ")
    eleStyle.SetTitleXOffset(1.0)
    eleStyle.SetTitleYOffset(1.0)
    eleStyle.SetLabelOffset(0.005, "XYZ") # numeric label
    eleStyle.SetTitleSize(0.05, "XYZ")
    eleStyle.SetTitleFont(22,"X")
    eleStyle.SetTitleFont(22,"Y")
    eleStyle.SetPadBottomMargin(0.13)
    eleStyle.SetPadLeftMargin(0.15)
    eleStyle.SetPadRightMargin(0.2) 
    eleStyle.SetMarkerStyle(21)
    eleStyle.SetMarkerSize(0.8)
    eleStyle.cd()
    ROOT.gROOT.ForceStyle()

def createPicture2(histo1, histo2, scaled, err, filename, cnv, axisFormat):
    nbins1 = histo1.GetNbinsX()
    nbins2 = histo2.GetNbinsX()
    new_entries = histo1.Integral(0,nbins1+1)
    ref_entries = histo2.Integral(0,nbins2+1)

    if ((scaled =="1") and (new_entries != 0) and (ref_entries != 0)):
        rescale_factor = new_entries / ref_entries
        histo2.Scale(rescale_factor)
    if (histo2.GetMaximum() > histo1.GetMaximum()):
        histo1.SetMaximum(histo2.GetMaximum() * 1.1)
    if (filename == "h_ele_charge"):
       n_ele_charge = histo1.GetEntries()
       
    cnv.SetCanvasSize(960, 900)
    cnv.Clear()
    cnv.SetFillColor(10)
    
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.25, 1, 1.0)
    pad1.SetBottomMargin(0.05)
    pad1.Draw()
    pad1.cd()

    if err == "1":
        newDrawOptions ="E1 P"
    else:
        newDrawOptions = "hist"

    histo1.SetStats(1)
    histo1.Draw(newDrawOptions)
    RenderHisto(histo1, cnv)
    if (axisFormat == "log" and histo1.GetMaximum() > 0):
        pad1.SetLogy(1)
    gPad.Update()
    statBox1 = histo1.GetListOfFunctions().FindObject("stats")
    statBox1.SetTextColor(ROOT.kRed)
    gPad.Update()
    histo2.Draw("sames hist")
    histo2.SetStats(1)
    RenderHisto(histo2, cnv)
    if (axisFormat == "log" and histo2.GetMaximum() > 0):
        pad1.SetLogy(1)
    cnv.Update()
    statBox2 = histo2.GetListOfFunctions().FindObject("stats")
    statBox2.SetTextColor(ROOT.kBlue)
    y1 = statBox1.GetY1NDC()
    y2 = statBox1.GetY2NDC()
    statBox2.SetY1NDC(2*y1-y2)
    statBox2.SetY2NDC(y1)
    newDrawOptions = "sames "
    if err == "1":
        newDrawOptions += "E1 P"
    else:
        newDrawOptions += "hist"
    histo1.Draw(newDrawOptions)
    histo2.Draw("sames hist")

    cnv.cd()
    # Define the ratio plot between histo1 and histo2
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.25)
    pad2.SetTopMargin(0.025)
    pad2.SetBottomMargin(0.2)
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    
    # Clone histo1
    histo3 = histo1.Clone("histo3")
    histo3.SetLineColor(ROOT.kBlack)
    histo3.SetMaximum(2.)
    histo3.SetStats(0)
    # Compare to histo2
    histo3.Divide(histo2)
    histo3.SetMarkerStyle(21)
    histo3.Draw("ep")
    
    histo1.SetMarkerColor(ROOT.kRed)
    histo1.SetLineWidth(3) 
    histo1.SetLineColor(ROOT.kRed)
    histo1.GetYaxis().SetTitleSize(25)
    histo1.GetYaxis().SetTitleFont(43)
    histo1.GetYaxis().SetTitleOffset(2.00)
    
    histo2.SetLineColor(ROOT.kBlue)
    histo2.SetMarkerColor(ROOT.kBlue)
    histo2.SetLineWidth(3) 
    
    histo3.SetTitle("")
    # Y axis ratio plot settings
    histo3.GetYaxis().SetTitle("ratio h1/h2 ")
    histo3.GetYaxis().SetNdivisions(505)
    histo3.GetYaxis().SetTitleSize(20)
    histo3.GetYaxis().SetTitleFont(43)
    histo3.GetYaxis().SetTitleOffset(1.55)
    histo3.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
    histo3.GetYaxis().SetLabelSize(15)
    # X axis ratio plot settings
    histo3.GetXaxis().SetTitleSize(20)
    histo3.GetXaxis().SetTitleFont(43)
    histo3.GetXaxis().SetTitleOffset(4.)
    histo3.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
    histo3.GetXaxis().SetLabelSize(15)
   
    cnv.Draw()
    cnv.Update()

    cnv.SaveAs(filename)
    
    return

def createWebPageLite(refconfigname, testconfigname, refdir, testdir, imgdir):
    print('Start creating web pages, ', ref_configname, ' - ' , test_configname)
    
    # graphical initialization
    initRootStyle()
    cnv = TCanvas("canvas")
    
    if os.path.exists(imgdir):
      print("The path " + imgdir + "exists. Will be deleted.")
      os.system("rm -rf " + imgdir)
      
    os.system("mkdir " + imgdir)
    os.system("mkdir " + imgdir + "/img")
    
    # Files names
    filename_ref = "/DQM_V0001_validation_HGCAL_TPG_" + refconfigname + "_ref_R000000001.root"
    filename_test = "/DQM_V0001_validation_HGCAL_TPG_" + testconfigname + "_test_R000000001.root"
    input_ref_file = refdir + filename_ref
    input_test_file = testdir + filename_test
    path_1 = 'DQMData/Run 1/HGCALTPG/Run summary'
    path_2 = path_1
    print('input_ref_file=', input_ref_file)
    print('input_test_file=', input_test_file)
    
    f_test = ROOT.TFile(input_test_file)
    h1 = getHisto(f_test, path_1)
    h1.ls()
    
    f_ref = ROOT.TFile(input_ref_file)
    h2 = getHisto(f_ref, path_2)
    h2.ls()
    
    CMP_CONFIG = '../HGCTPGValidation/data/HGCALTriggerPrimitivesHistos.txt'
    CMP_TITLE = ' HGCAL Trigger Primitives Validation '
    CMP_RED_FILE = input_test_file
    CMP_BLUE_FILE = input_ref_file
    CMP_INDEX_FILE_DIR = webdir + '/index.html'
                     
    MEM_REP_REF = './MemoryReport_' + ref_configname + '_ref.log'
    MEM_REP_TEST = './MemoryReport_' + test_configname + '_test.log'
    
    shutil.copy2('../HGCTPGValidation/data/img/up.gif', webdir+ '/img')
    shutil.copy2('../HGCTPGValidation/data/img/point.gif', webdir+ '/img')
    image_up = './img/up.gif'
    image_point = './img/point.gif'
    
    f = open(CMP_CONFIG, 'r')
    fmemref = open(MEM_REP_REF, 'r')
    fmemtest = open(MEM_REP_TEST, 'r')
    
    wp = open(CMP_INDEX_FILE_DIR, 'w') # web page
    wp.write("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\">\n")
    wp.write("<html>\n")
    wp.write("<head>\n")
    wp.write("<meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\" />\n")
    wp.write("<title> " + CMP_TITLE + " </title>\n") #option -t dans OvalFile
    wp.write("</head>\n")
    wp.write("<a NAME=\"TOP\"></a>")
    wp.write("<h1><a href=\"../\"><img border=0 width=\"22\" height=\"22\" src=\"img/up.gif\" alt=\"Up\"/></a>&nbsp; " + CMP_TITLE + " </h1>\n" ) # option -t dans OvalFile
        
    # here you can add some text such as GlobalTag for release & reference.
    wp.write("<br>\n")

    filePath='../HGCTPGValidation/config/'
    test_configData=read_config(filePath, test_configname, 1)
    test_description=test_configData['description']
    ref_configData=read_config(filePath, ref_configname, 1)
    ref_description=ref_configData['description']
    
    # get time 
    # dd/mm/YY H:M:S
    now = datetime.now()
    time = now.strftime("%d/%m/%Y %H:%M:%S")

    # Comment not needed informations
    if (f_ref == 0):
        wp.write("<p>In all plots below, there was no reference histograms to compare with")
        wp.write(", and the " + CMP_RED_FILE + " histograms are in red.") # new release red in OvalFile
    else:
        wp.write("<h3><p><font color='black'> Generated " + time + "</h3><p>")
        wp.write("<h3><p><font color='red'> Test: " + test_configname + "</h3>")
        wp.write("<p>" + test_description )
        wp.write("<h3><p><font color='blue'> Ref: " + ref_configname + "</h3>" )
        wp.write("<p>" + ref_description )
        wp.write("<p><font color='black'>=====================")
    #    wp.write("<p>In all plots below " + test_configname)
    #    wp.write(", the <b><font color='red'> " + CMP_RED_FILE + " </font></b> histograms are in red") # new release red in OvalFile
    #    wp.write(", and the <b><font color='blue'> " + CMP_BLUE_FILE + " </font></b> histograms are in blue.") # ref release blue in OvalFile
    #wp.write(" Some more details") # 
    #wp.write(", <a href=\"" + CMP_CONFIG + "\">specification</a> of histograms") # histos list .txt file
    #wp.write(", <a href=\"gifs/\">images</a> of histograms" + "." )
    wp.write("</p>\n")

    # filling the title array & dict
    histoArray_0 = {}
    titlesList = [] # need with python < 3.7. dict does not keep the correct order of the datasets histograms
    key = ""
    tmp = []
    for line in f:
        print('line = ', line)
        if ( len(line) == 1 ): # len == 0, empty line
            if ( ( len(key) != 0 ) and ( len(tmp) != 0) ): 
                histoArray_0[key] = tmp
                key = ""
                tmp = []
        else: # len <> 0
            if ( len(key) == 0 ):
                key = line # get title
                titlesList.append(line)
            else:
                tmp.append(line) # histo name
    # end of filling the title array & dict
    f.close()
    wp.write( "<table border=\"1\" cellpadding=\"5\" width=\"100%\">" )
    
    for i in range(0, len(titlesList)):
        if ( i % 5  == 0 ):
            wp.write( "\n<tr valign=\"top\">" )
        textToWrite = ""
        wp.write( "\n<td width=\"10\">\n<b> " + titlesList[i] + "</b>" )
        titles = titlesList[i].split()
        if len(titles) > 1 :
            titleShortName = titles[0] + "_" + titles[1]
        else:
            titleShortName = titles[0]
        wp.write( "&nbsp;&nbsp;" + "<a href=\"#" + titleShortName + "\">" ) # write group title
        wp.write( "<img width=\"18\" height=\"15\" border=\"0\" align=\"center\" src=" + image_point + " alt=\"Top\"/>" + "<br><br>" )
        textToWrite += "</a>"
        histoPrevious = ""
        numLine = 0
            
        for elem in histoArray_0[titlesList[i]]:
            otherTextToWrite = ""
            histo_names = elem.split("/")
            histoShortNames = histo_names[0]
            short_histo_names = histoShortNames.split(" ")
            histo_name = short_histo_names[0].strip().replace('\n', ' ').replace('\r', '')
            print('!!!!! histo_name = ',histo_name)
            short_histo_name = histo_name.replace("h_", "")
            if "ele_" in short_histo_name:
                short_histo_name = short_histo_name.replace("ele_", "")
            if "scl_" in short_histo_name:
                short_histo_name = short_histo_name.replace("scl_", "")
            if "bcl_" in short_histo_name:
                short_histo_name = short_histo_name.replace("bcl_", "")
                   
            otherTextToWrite += "<a href=\"#" + short_histo_name + "\"><font color=\'blue\'>" + short_histo_name + "</font></a>" + "&nbsp;\n"
                    
            otherTextToWrite += "<br>"
            otherTextToWrite = otherTextToWrite.replace("<br><br>", "<br>")

            textToWrite += otherTextToWrite
        textReplace = True
        while textReplace :
            textToWrite = textToWrite.replace("<br><br>", "<br>")
            if ( textToWrite.count('<br><br>') >= 1 ):
                textReplace = True
            else:
                textReplace = False
        if ( textToWrite.count("</a><br><a") >= 1 ):
                textToWrite = textToWrite.replace("</a><br><a", "</a><a")
        wp.write( textToWrite )
                    
        wp.write( "</td>" )
        if ( i % 5 == 4 ):
            wp.write( "</tr>" )
              
    wp.write( "</table>\n" )
    wp.write( "<br>" )
    
    memInfoRef = []
    memInfoTest = []
    i=0
    with open(MEM_REP_REF) as file:
        for line in file.readlines():
            memInfoRef.append(line)
            ++i
 
    with open(MEM_REP_TEST) as file:
        for line in file.readlines():
            memInfoTest.append(line)
            ++i
            
    # Write Memory and Timing Summary into a table
    wp.write( "<h2>" + " Memory and Timing Summary" + "</h2>\n" )
    wp.write( "<style>" )
    wp.write( "table, th, td {" )
    wp.write( "border:1px solid black;" )
    wp.write( "}" )
    wp.write( "</style>" )
    wp.write( "<table style=\"width:100%\">" )
    wp.write( "  <tr>" )
    wp.write( "    <th>  </th>" )
    wp.write( "    <th><font color='blue'> Ref</th>" )
    wp.write( "    <th><font color='red'> Test</th>" )
    wp.write( "  </tr>" )
    wp.write( "  <tr>" )
    wp.write( "    <th>Peak Memory</th>" )
    wp.write( "    <th> <font color='blue'>" + memInfoRef[0] + "</th>" )
    wp.write( "    <th><font color='red'>" + memInfoTest[0] + "</th>" )
    wp.write( "  </tr>" )
    wp.write( "  <tr>" )
    wp.write( "    <th>Time Avg event</th>" )
    wp.write( "    <th><font color='blue'>" + memInfoRef[1] + "</th>" )
    wp.write( "    <th><font color='red'>" + memInfoTest[1] + "</th>" )
    wp.write( "  </tr>" )
    wp.write( "  <tr>" )
    wp.write( "    <th>Total loop</th>" )
    wp.write( "    <th><font color='blue'>" + memInfoRef[2] + "</th>" )
    wp.write( "    <th><font color='red'>" + memInfoTest[2] + "</th>" )
    wp.write( "  </tr>" )
    wp.write( "  <tr>" )
    wp.write( "    <th>Total init</th>" )
    wp.write( "    <th><font color='blue'>" + memInfoRef[3] + "</th>" )
    wp.write( "    <th><font color='red'>" + memInfoTest[3] + "</th>" )
    wp.write( "  </tr>" )
    wp.write( "</table>\n" )
    wp.write( "<br>" )
    wp.write( "<br>" )
    wp.write( "<table border=\"0\" cellpadding=\"5\" width=\"100%\">" )
    for i in range(0, len(titlesList)):
        wp.write( "\n<tr valign=\"top\">" )
        wp.write( "\n<td><a href=\"#TOP\"><img width=\"18\" height=\"18\" border=\"0\" align=\"middle\" src=" + image_up + " alt=\"Top\"/></a></td>\n" )
        titles = titlesList[i].split()
        if len(titles) > 1 :
            titleShortName = titles[0] + "_" + titles[1]
        else:
            titleShortName = titles[0]
        wp.write( "\n<td>\n<b> " )
        wp.write( "<a id=\"" + titleShortName + "\" name=\"" + titleShortName + "\"></a>" )
        wp.write( titlesList[i] + "</b></td>" )
        wp.write( "</tr><tr valign=\"top\">" )
        for elem in histoArray_0[titlesList[i]]:
            if ( elem != "endLine" ):
                histo_names = elem.split("/")
                histoShortNames = histo_names[0]
                short_histo_names = histoShortNames.split(" ")
                histo_name = short_histo_names[0].strip().replace('\n', ' ').replace('\r', '')
                short_histo_name = histo_name.replace("h_", "")
                if "ele_" in short_histo_name:
                    short_histo_name = short_histo_name.replace("ele_", "")
                if "scl_" in short_histo_name:
                    short_histo_name = short_histo_name.replace("scl_", "")
                if "bcl_" in short_histo_name:
                    short_histo_name = short_histo_name.replace("bcl_", "")
                
                histo_2 = h2.Get(histo_name)
                histo_1 = h1.Get(histo_name)
                
                # Change the name of the histograms
                histo_2.SetName(histo_name + " - ref")
                histo_1.SetName(histo_name + " - test")
                
                gif_name = webdir + '/' + histo_name + ".gif"
                gif_name_index = histo_name + ".gif"
                createPicture2(histo_1, histo_2, "1", "1", gif_name, cnv, "lin")
                # Make histo in log
                #if (histo_1.GetMaximum() > 0 and histo_1.GetMinimum() >= 0):
                #    gif_name_log = webdir + '/' + histo_name + "_log.gif"
                #    gif_name_log_index = histo_name + "_log.gif"
                #    createPicture2(histo_1, histo_2, "1", "1", gif_name_log, cnv, "log")

                wp.write( "\n<td><a href=\"#TOP\"><img width=\"18\" height=\"18\" border=\"0\" align=\"middle\" src=" + image_up + " alt=\"Top\"/></a></td>\n" )
                wp.write( "<td>" )
                wp.write( "<a id=\"" + short_histo_name + "\" name=\"" + short_histo_name + "\"></a>" )
                wp.write( "<a href=\"" + gif_name_index + "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" + gif_name_index + "\"></a>" )
                # For histo in log
                #if (histo_1.GetMaximum() > 0 and histo_1.GetMinimum() >= 0):
                #    wp.write( "</td><td><a href=\"" + gif_name_log_index + "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" + gif_name_log_index + "\"></a>" )
                wp.write( "</td></tr><tr valign=\"top\">\n" )
    
    wp.write( "</tr></table>\n" )
    wp.close()
        
    return
    
def testExtension(histoName, histoPrevious):
    after = "" # $histoName
    common = ""
    
    if '_' in histoName:
        afters = histoName.split('_')
        before = afters[0]
        nMax = len(afters)
        
        if ( afters[nMax - 1] == "endcaps" ):
            after = "endcaps"
            for i in range(1, nMax-1):
                before += "_" + afters[i]
        elif ( afters[nMax - 1] == "barrel" ):
            after = "barrel"
            for i in range(1, nMax-1):
                before += "_" + afters[i]
        else:
            if ( histoPrevious == "" ):
                before = histoName
                after = "" 
                common = histoName
            else:
                avant =  afters[0]
                after = ""
                for i in range(1, nMax-1):
                    avant += "_" + afters[i]
                    if avant == histoPrevious:
                        before = avant
                        common = histoPrevious
                        break
                for j in range(nMax-1, nMax):
                    after += "_" + afters[j]
                after = after[1:]
                
    else: # no _ in histoName
        before = histoName
        common = histoName
    
    return [after, before, common]

def checkRecompInName(name):
    if re.search('recomp', name):
        return True
    else:
        return False

