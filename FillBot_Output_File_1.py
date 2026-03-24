from opentrons import protocol_api, types

metadata = {
    "protocolName": "Auto Generated FillBot Protocol",
    "apiLevel": "2.15"
}


def run(protocol: protocol_api.ProtocolContext):

    DMSO_plate = protocol.load_labware(
        "corning_384_wellplate_112ul_flat", "2"
    )

    aqueous_reservoir = protocol.load_labware(
        "nest_1_reservoir_195ml", "6"
    )

    tiprack_20 = protocol.load_labware(
        "opentrons_96_tiprack_20ul", "4"
    )
    
    tiprack_1000 = protocol.load_labware(
        "opentrons_96_tiprack_1000ul", "1"
    )

    mix_plate = protocol.load_labware(
        "corning_96_wellplate_360ul_flat", "5"
    )


    NMR_rack = protocol.load_labware(
        "nest_96_wellplate_2ml_deep", "8"
    )

    eppendorf_plate = protocol.load_labware(
        "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap", "9"
    )

    pipette_20 = protocol.load_instrument(
        "p20_single_gen2",
        "left",
        tip_racks=[tiprack_20]
    )
    pipette_1000 = protocol.load_instrument(
        "p1000_single_gen2",
        "right",
        tip_racks=[tiprack_1000]
    )
    # ← injected automatically
    combined_data = [{'well': 'A1', 'sample_id': 'Drug 1', 'location_384': 'A6', 'vol_384': '3', 'location_eppendorf': 'A3', 'vol_eppendorf': '10', 'vol_aqueous': '100'}]
    wells = ['A1']
    sample_ids = ['Drug 1']
    location_384 = ['A6']
    vol_384 = ['3']
    location_eppendorf = ['A3']
    vol_eppendorf = ['10']
    vol_aqueous = ['100']

    p20_offset = {
        "aspirate": {"x": 0, "y": 0, "z": 0},
        "dispense": {"x": 0, "y": 0, "z": 0},
    }
    p1000_buffer_offset = {
        "aspirate": {"x": 0, "y": 0, "z": 0},
        "dispense": {"x": 0, "y": 0, "z": 0},
        "mix": {"x": 0, "y": 0, "z": 0},
    }
    p1000_nmr_offset = {
        "aspirate": {"x": 0, "y": 0, "z": 0},
        "dispense": {"x": 0, "y": 0, "z": 0},
        "mix": {"x": 0, "y": 0, "z": 0},
    }

    protocol.comment(f"Wells: {wells}")
    protocol.comment(f"Sample IDs: {sample_ids}")
    protocol.comment(f"Combined data: {combined_data}")

    # Pick up tip once for p1000 and keep it throughout, change to none eventually
  

    


    for i, well in enumerate(wells):
        
        #DMSO Transfer
        pipette_20.pick_up_tip()
        source_well = DMSO_plate.wells_by_name()[location_384[i]]
        dest_well = mix_plate.wells_by_name()[well]
        aspirate_loc = source_well.top().move(types.Point(x=p20_offset["aspirate"]["x"], y=p20_offset["aspirate"]["y"], z=p20_offset["aspirate"]["z"]))
        dispense_loc = dest_well.top().move(types.Point(x=p20_offset["dispense"]["x"], y=p20_offset["dispense"]["y"], z=p20_offset["dispense"]["z"]))
        pipette_20.aspirate(float(vol_384[i]), aspirate_loc)
        pipette_20.dispense(float(vol_384[i]), dispense_loc)
        pipette_20.drop_tip()

        #Buffer Transfer
        pipette_1000.pick_up_tip()
        source_well = aqueous_reservoir.wells()[0]
        dest_well = mix_plate.wells_by_name()[well]
        aspirate_loc = source_well.top().move(types.Point(x=p1000_buffer_offset["aspirate"]["x"], y=p1000_buffer_offset["aspirate"]["y"], z=p1000_buffer_offset["aspirate"]["z"]))
        dispense_loc = dest_well.top().move(types.Point(x=p1000_buffer_offset["dispense"]["x"], y=p1000_buffer_offset["dispense"]["y"], z=p1000_buffer_offset["dispense"]["z"]))
        mix_loc = dest_well.top().move(types.Point(x=p1000_buffer_offset["mix"]["x"], y=p1000_buffer_offset["mix"]["y"], z=p1000_buffer_offset["mix"]["z"]))
        pipette_1000.aspirate(float(vol_aqueous[i]), aspirate_loc)
        pipette_1000.dispense(float(vol_aqueous[i]), dispense_loc)
        pipette_1000.mix(3, 100, mix_loc)
        
        
        #Eppendorf Transfer
        pipette_20.pick_up_tip()
        vol_epp = float(vol_eppendorf[i])
        while vol_epp > 0:
            transfer_vol = min(vol_epp, 20)
            source_well = eppendorf_plate[location_eppendorf[i]]
            dest_well = mix_plate.wells_by_name()[well]
            aspirate_loc = source_well.top().move(types.Point(x=p20_offset["aspirate"]["x"], y=p20_offset["aspirate"]["y"], z=p20_offset["aspirate"]["z"]))
            dispense_loc = dest_well.top().move(types.Point(x=p20_offset["dispense"]["x"], y=p20_offset["dispense"]["y"], z=p20_offset["dispense"]["z"]))
            pipette_20.aspirate(transfer_vol, aspirate_loc)
            pipette_20.dispense(transfer_vol, dispense_loc)
            vol_epp -= transfer_vol
        pipette_20.drop_tip()

    protocol.pause("Attach NMR Rack")

    pipette_1000.pick_up_tip
    for i, well in enumerate(wells):
        #Moving to NMR rack
        source_well = mix_plate.wells_by_name()[well]
        dest_well = NMR_rack.wells_by_name()[well]
        mix_loc = source_well.top().move(types.Point(x=p1000_nmr_offset["mix"]["x"], y=p1000_nmr_offset["mix"]["y"], z=p1000_nmr_offset["mix"]["z"]))
        aspirate_loc = source_well.top().move(types.Point(x=p1000_nmr_offset["aspirate"]["x"], y=p1000_nmr_offset["aspirate"]["y"], z=p1000_nmr_offset["aspirate"]["z"]))
        dispense_loc = dest_well.top().move(types.Point(x=p1000_nmr_offset["dispense"]["x"], y=p1000_nmr_offset["dispense"]["y"], z=p1000_nmr_offset["dispense"]["z"]))
        pipette_1000.mix(3, 100, mix_loc)
        pipette_1000.aspirate(100, aspirate_loc)
        pipette_1000.dispense(100, dispense_loc)

    # Drop p1000 tip after all transfers complete
    pipette_1000.drop_tip()


