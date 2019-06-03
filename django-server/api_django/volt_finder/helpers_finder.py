def match_cs_nk_based_on_address(gg_top_cs, cs_list):
    for item in gg_top_cs:
        cs_nk = next((cs.nk for cs in cs_list if cs.address ==
                      item.destination_addresses), None)
        if cs_nk is not None:
            item.nk = str(cs_nk)
        else:
            pass
