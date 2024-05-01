
#v001
# base on the CamDissolve v007 and make it as nuke 12 version


def CameraDissolve():

    # select nodes
    sNodes = nuke.selectedNodes()
    
    # get the information from the selected Nodes



    ## check error

    # if select No nodes
    if len(sNodes)!=2:
        nuke.message('Please select only two Camera')
        return()
            


    # Get Camera
    aCamNode = sNodes[-1]
    bCamNode = sNodes[0]

    # Get Camera Name 
    aCamName = aCamNode.name()
    bCamName = bCamNode.name()


    print (aCamNode.name())
    print (bCamNode.name())

    # DisSelected Node
    for node in sNodes:
        node['selected'].setValue(0)

    # Create new Camera
    nCamera = nuke.createNode('Camera3')
    
    nCamera['xpos'].setValue(((aCamNode['xpos'].getValue()+bCamNode['xpos'].getValue())/2)+0)
    nCamera['ypos'].setValue(((aCamNode['ypos'].getValue()+bCamNode['ypos'].getValue())/2)+300)
    
    nCamera['tile_color'].setValue(0xff00bfff)
    nCamera['gl_color'].setValue(0xff00bfff)
    nCamera['label'].setValue('CameraDissolve')

    # Deselected All nodes
    for n in nuke.allNodes():
        n.knob("selected").setValue(False) 

    
    # Create Retimed A Cam

    refACam = nuke.createNode('Camera3')
    
    refACam['xpos'].setValue(aCamNode['xpos'].getValue()+0)
    refACam['ypos'].setValue(aCamNode['ypos'].getValue()+150)
    
    
    refACam['tile_color'].setValue(int(aCamNode['tile_color'].getValue()))
    refACam['gl_color'].setValue(int(aCamNode['tile_color'].getValue()))
    refACam['label'].setValue('Retimed A Cam') 

    # Deselected All nodes
    for n in nuke.allNodes():
        n.knob("selected").setValue(False) 

    
    # Create Retimed B Cam
    refBCam = nuke.createNode('Camera3')
    
    refBCam['xpos'].setValue(bCamNode['xpos'].getValue()+0)
    refBCam['ypos'].setValue(bCamNode['ypos'].getValue()+150)
    
    
    refBCam['tile_color'].setValue(int(bCamNode['tile_color'].getValue()))
    refBCam['gl_color'].setValue(int(bCamNode['tile_color'].getValue()))
    refBCam['label'].setValue('Retimed B Cam')    

    # Deselected All nodes
    for n in nuke.allNodes():
        n.knob("selected").setValue(False) 

    

    # Create custom CamDissove tag and knobs 

    camMixSliderTab = nuke.Tab_Knob('cameraDissolveTab', 'CamDissolve')
    aCamTimeOffsetknob = nuke.Int_Knob('aCameraOffset', 'A Cam Time Offset',0)
    bCamTimeOffsetknob = nuke.Int_Knob('bCameraOffset', 'B Cam Time Offset',0)   
    camMixSliderKnob = nuke.Double_Knob('camDissolve','Camera Dissolve')
    #aCamRetimed = nuke.PyScript_Knob('aCamRetimed','Create Retimed A Cam',aCamRetimePyContent)
    #bCamRetimed = nuke.PyScript_Knob('bCamRetimed','Create Retimed B Cam',bCamRetimePyContent)   


    # Collect all the knob as List for Dissolve node

    panelKnobs = [camMixSliderTab,aCamTimeOffsetknob,bCamTimeOffsetknob,camMixSliderKnob]


    #Create Retimed A Cam knobs
    camMixSliderTab_ACam = nuke.Tab_Knob('cameraDissolveTab', 'CamDissolve')
    aCamTimeOffsetknob_ACam = nuke.Int_Knob('aCameraOffset', 'A Cam Time Offset',0)
    bCamTimeOffsetknob_ACam = nuke.Int_Knob('bCameraOffset', 'B Cam Time Offset',0)  
    camMixSliderKnob_ACam = nuke.Double_Knob('camDissolve','Camera Dissolve')

    # Collect a Cam knobs
    panelKnobs_ACam = [camMixSliderTab_ACam,aCamTimeOffsetknob_ACam,bCamTimeOffsetknob_ACam,camMixSliderKnob_ACam]

    #Create Retimed B Cam knobs
    camMixSliderTab_BCam = nuke.Tab_Knob('cameraDissolveTab', 'CamDissolve')
    aCamTimeOffsetknob_BCam = nuke.Int_Knob('aCameraOffset', 'A Cam Time Offset',0)
    bCamTimeOffsetknob_BCam = nuke.Int_Knob('bCameraOffset', 'B Cam Time Offset',0)  
    camMixSliderKnob_BCam = nuke.Double_Knob('camDissolve','Camera Dissolve')

    # Collect a Cam knobs
    panelKnobs_BCam = [camMixSliderTab_BCam,aCamTimeOffsetknob_BCam,bCamTimeOffsetknob_BCam,camMixSliderKnob_BCam]


    # Add all the knobs to Panel 
    
    for panelKnob in panelKnobs:
        nCamera.addKnob(panelKnob) 

    for panelKnobRefACam in panelKnobs_ACam:
        refACam.addKnob(panelKnobRefACam) 
    

    for panelKnobRefBCam in panelKnobs_BCam:
        refBCam.addKnob(panelKnobRefBCam) 
    

   

    # Get All The Knob Would Like to Blend

    knobsList =[
    'translate','rotate','scaling','uniform_scale','skew',
    'pivot_translate','pivot_rotate','focal','haperture','vaperture',
    'near','far','win_translate','win_scale','winroll','focal_point','fstop'
    ]




    for knob in knobsList:
        
        nCamera[knob].setExpression('lerp({}.{}{},{}.{}{},{})'.format(aCamName,knob,'(frame-aCameraOffset)',bCamName,knob,'(frame-bCameraOffset)','camDissolve'))
        refACam[knob].setExpression('lerp({}.{}{},{}.{}{},{})'.format(aCamName,knob,'(frame-aCameraOffset)',bCamName,knob,'(frame-bCameraOffset)','camDissolve'))
        refBCam[knob].setExpression('lerp({}.{}{},{}.{}{},{})'.format(aCamName,knob,'(frame-aCameraOffset)',bCamName,knob,'(frame-bCameraOffset)','camDissolve'))
    
    # expression linked To Dissolved Camera
    

    ## Retimed A cam Setup Value
    # Link time offset to Dissolve Camera node
    refACam['aCameraOffset'].setExpression('parent.%s.aCameraOffset'%nCamera.name())
    refACam['bCameraOffset'].setExpression('parent.%s.bCameraOffset'%nCamera.name())
    refACam['camDissolve'].setValue(0) # set value to 0 so, value match A cam 


    refACam['aCameraOffset'].setEnabled(False)    # disable all parameter
    refACam['bCameraOffset'].setEnabled(False)
    refACam['camDissolve'].setEnabled(False)

    ## Retimed B cam Setup Value
    refBCam['aCameraOffset'].setExpression('parent.%s.aCameraOffset'%nCamera.name())
    refBCam['bCameraOffset'].setExpression('parent.%s.bCameraOffset'%nCamera.name())
    refBCam['camDissolve'].setValue(1)# set value to 1 so, value match B cam 

    refBCam['aCameraOffset'].setEnabled(False)
    refBCam['bCameraOffset'].setEnabled(False)
    refBCam['camDissolve'].setEnabled(False)

CameraDissolve()



