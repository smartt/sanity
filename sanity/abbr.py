
__license__ = "MIT"
__version__ = "0.1"
__url__ = "http://github.com/smartt/sanity"
__doc__ = "A collection of misguided hacks."


STATE_MAP = {
    'A.S.': ('American Samoa'),
    'AA': ('Armed Forces Americas'),
    'AE': ('Armed Forces'),
    'AK': ('Alaska'),
    'AL': ('Alabama'),
    'Ala.': ('Alabama'),
    'Alas.': ('Alaska'),
    'AP': ('Armed Forces Pacific'),
    'AR': ('Arkansas'),
    'Ariz.': ('Arizona'),
    'Ark.': ('Arkansas'),
    'AS': ('American Samoa'),
    'AZ': ('Arizona'),
    'Az.': ('Arizona'),
    'C.Z.': ('Canal Zone'),
    'CA': ('California'),
    'Ca.': ('California'),
    'Cal.': ('California'),
    'Cali.': ('California'),
    'Calif.': ('California'),
    'CF': ('California'),
    'CL': ('Colorado'),
    'CM': ('Commonwealth of the Northern Mariana Islands', 'Northern Mariana Islands'),
    'CO': ('Colorado'),
    'Col.': ('Colorado'),
    'Colo.': ('Colorado'),
    'Conn.': ('Connecticut'),
    'CT': ('Connecticut'),
    'Ct.': ('Connecticut'),
    'CZ': ('Canal Zone'),
    'D.C.': ('District of Columbia'),
    'DC': ('District of Columbia'),
    'DE': ('Delaware'),
    'De.': ('Delaware'),
    'Del.': ('Delaware'),
    'DL': ('Delaware'),
    'FL': ('Florida'),
    'Fl.': ('Florida'),
    'Fla.': ('Florida'),
    'Flor.': ('Florida'),
    'FM': ('Federated States of Micronesia'),
    'GA': ('Georgia'),
    'Ga.': ('Georgia'),
    'GU': ('Guam'),
    'H.I.': ('Hawaii'),
    'HA': ('Hawaii'),
    'HI': ('Hawaii'),
    'IA': ('Iowa'),
    'Ia.': ('Iowa'),
    'ID': ('Idaho'),
    'Id.': ('Idaho'),
    'Ida.': ('Idaho'),
    'IL': ('Illinois'),
    'Ill.': ('Illinois'),
    'Ill\'s.': ('Illinois'),
    'Ills.': ('Illinois'),
    'IN': ('Indiana'),
    'In.': ('Indiana'),
    'Ind.': ('Indiana'),
    'Ioa.': ('Iowa'),
    'KA': ('Kansas'),
    'Ka.': ('Kansas'),
    'Kan.': ('Kansas'),
    'Kans.': ('Kansas'),
    'Ken.': ('Kentucky'),
    'Kent.': ('Kentucky'),
    'KS': ('Kansas'),
    'Ks.': ('Kansas'),
    'KY': ('Kentucky'),
    'Ky.': ('Kentucky'),
    'LA': ('Louisiana'),
    'La.': ('Louisiana'),
    'M.P.': ('Northern Mariana Islands'),
    'MA': ('Massachusetts'),
    'Mass.': ('Massachusetts'),
    'MC': ('Michigan'),
    'MD': ('Maryland'),
    'Md.': ('Maryland'),
    'ME': ('Maine'),
    'Me.': ('Maine'),
    'MH': ('Marshall Islands'),
    'MI': (('Michigan', 'Mississippi')),
    'Mich.': ('Michigan'),
    'Minn.': ('Minnesota'),
    'Miss.': ('Mississippi'),
    'MN': ('Minnesota'),
    'Mn.': ('Minnesota'),
    'MO': ('Missouri'),
    'Mo.': ('Missouri'),
    'Mont.': ('Montana'),
    'MP': (('Commonwealth of the Northern Mariana Islands', 'Northern Mariana Islands')),
    'MS': (('Massachusetts', 'Mississippi')),
    'MT': ('Montana'),
    'N. Car.': ('North Carolina'),
    'N. Dak.': ('North Dakota'),
    'N. Mex.': ('New Mexico'),
    'N. York': ('New York'),
    'N.C.': ('North Carolina'),
    'N.D.': ('North Dakota'),
    'N.H.': ('New Hampshire'),
    'N.J.': ('New Jersey'),
    'N.M.': ('New Mexico'),
    'N.Y.': ('New York'),
    'NB': ('Nebraska'),
    'NC': ('North Carolina'),
    'ND': ('North Dakota'),
    'NE': ('Nebraska'),
    'Neb.': ('Nebraska'),
    'Nebr.': ('Nebraska'),
    'Nev.': ('Nevada'),
    'New M.': ('New Mexico'),
    'NH': ('New Hampshire'),
    'NJ': ('New Jersey'),
    'NM': ('New Mexico'),
    'NV': ('Nevada'),
    'Nv.': ('Nevada'),
    'NY': ('New York'),
    'O.': ('Ohio'),
    'OH': ('Ohio'),
    'Oh.': ('Ohio'),
    'OK': ('Oklahoma'),
    'Ok.': ('Oklahoma'),
    'Okla.': ('Oklahoma'),
    'OR': ('Oregon'),
    'Or.': ('Oregon'),
    'Ore.': ('Oregon'),
    'Oreg.': ('Oregon'),
    'P.P.': ('Rhode Island'),
    'P.R.': ('Puerto Rico'),
    'PA': ('Pennsylvania'),
    'Pa.': ('Pennsylvania'),
    'Penn.': ('Pennsylvania'),
    'Penna.': ('Pennsylvania'),
    'PI': ('Philippine Islands'),
    'PR': ('Puerto Rico'),
    'PW': ('Palau'),
    'R.I.': ('Rhode Island'),
    'RI': ('Rhode Island'),
    'S. Car.': ('South Carolina'),
    'S. Dak.': ('South Dakota'),
    'S.C.': ('South Carolina'),
    'S.D.': ('South Dakota'),
    'SC': ('South Carolina'),
    'SD': ('South Dakota'),
    'Sodak': ('South Dakota'),
    'Tenn.': ('Tennessee'),
    'Tex.': ('Texas'),
    'TN': ('Tennessee'),
    'Tn.': ('Tennessee'),
    'TT': ('Trust Territory of the Pacific Islands'),
    'TX': ('Texas'),
    'U.S.V.I.': ('Virgin Islands'),
    'UM': ('U.S. Minor Outlying Islands'),
    'UT': ('Utah'),
    'Ut.': ('Utah'),
    'V.I.': ('Virgin Islands'),
    'VA': ('Virginia'),
    'Va.': ('Virginia'),
    'VI': ('Virgin Islands'),
    'Virg.': ('Virginia'),
    'VT': ('Vermont'),
    'Vt.': ('Vermont'),
    'W. Va.': ('West Virginia'),
    'W. Virg.': ('West Virginia'),
    'W.V.': ('West Virginia'),
    'W.Va.': ('West Virginia'),
    'WA': ('Washington'),
    'Wa.': ('Washington'),
    'Wash.': ('Washington'),
    'Wash., D.C.': ('District of Columbia'),
    'WI': ('Wisconsin'),
    'Wi.': ('Wisconsin'),
    'Wis.': ('Wisconsin'),
    'Wisc.': ('Wisconsin'),
    'WN': ('Washington'),
    'Wn.': ('Washington'),
    'WS': ('Wisconsin'),
    'WV': ('West Virginia'),
    'WY': ('Wyoming'),
    'Wy.': ('Wyoming'),
    'Wyo.': ('Wyoming'),
}


def us_state_for_abbr(s):
    """
    >>> us_state_for_abbr('TX')
    'Texas'

    >>> us_state_for_abbr('MS')
    'Massachusetts'

    """
    try:
        r = STATE_MAP[s]

    except KeyError:
        return s

    else:
        if isinstance(r, str):
            return r
        else:
            return r[0]


#--------------------------------------------------
#               MAIN
# --------------------------------------------------
if __name__ == "__main__":
    import doctest

    print('[abbr.py] Testing...')

    doctest.testmod()

    print('Done.')

