
__license__ = "MIT"
__version__ = "0.1"
__url__ = "http://github.com/smartt/sanity"
__doc__ = "A collection of misguided hacks."


STATE_MAP = [
    ('A.S.', ('American Samoa',)),
    ('AA', ('Armed Forces Americas',)),
    ('AE', ('Armed Forces',)),
    ('AK', ('Alaska',)),
    ('Alas.', ('Alaska',)),
    ('AL', ('Alabama',)),
    ('Ala.', ('Alabama',)),
    ('AS', ('American Samoa',)),
    ('AP', ('Armed Forces Pacific',)),
    ('AR', ('Arkansas',)),
    ('Ark.', ('Arkansas',)),
    ('AZ', ('Arizona',)),
    ('Az.', ('Arizona',)),
    ('Ariz.', ('Arizona',)),
    ('CZ', ('Canal Zone',)),
    ('C.Z.', ('Canal Zone',)),
    ('CA', ('California',)),
    ('Ca.', ('California',)),
    ('Cal.', ('California',)),
    ('Cali.', ('California',)),
    ('Calif.', ('California',)),
    ('CF', ('California',)),
    ('CO', ('Colorado',)),
    ('Col.', ('Colorado',)),
    ('Colo.', ('Colorado',)),
    ('CL', ('Colorado',)),
    ('CM', ('Commonwealth of the Northern Mariana Islands', 'Northern Mariana Islands',)),
    ('CT', ('Connecticut',)),
    ('Ct.', ('Connecticut',)),
    ('Conn.', ('Connecticut',)),
    ('D.C.', ('District of Columbia',)),
    ('DC', ('District of Columbia',)),
    ('DE', ('Delaware',)),
    ('De.', ('Delaware',)),
    ('Del.', ('Delaware',)),
    ('DL', ('Delaware',)),
    ('FL', ('Florida',)),
    ('Fl.', ('Florida',)),
    ('Fla.', ('Florida',)),
    ('Flor.', ('Florida',)),
    ('FM', ('Federated States of Micronesia',)),
    ('GA', ('Georgia',)),
    ('Ga.', ('Georgia',)),
    ('GU', ('Guam',)),
    ('H.I.', ('Hawaii',)),
    ('HA', ('Hawaii',)),
    ('HI', ('Hawaii',)),
    ('ID', ('Idaho',)),
    ('Id.', ('Idaho',)),
    ('Ida.', ('Idaho',)),
    ('IL', ('Illinois', 'IL - Illinois')),
    ('Ill.', ('Illinois',)),
    ('Ill\'s.', ('Illinois',)),
    ('Ills.', ('Illinois',)),
    ('IN', ('Indiana',)),
    ('In.', ('Indiana',)),
    ('Ind.', ('Indiana',)),
    ('IA', ('Iowa',)),
    ('Ia.', ('Iowa',)),
    ('Ioa.', ('Iowa',)),
    ('KA', ('Kansas',)),
    ('Ka.', ('Kansas',)),
    ('Kan.', ('Kansas',)),
    ('Kans.', ('Kansas',)),
    ('KS', ('Kansas',)),
    ('Ks.', ('Kansas',)),
    ('KY', ('Kentucky',)),
    ('Ken.', ('Kentucky',)),
    ('Kent.', ('Kentucky',)),
    ('Ky.', ('Kentucky',)),
    ('LA', ('Louisiana',)),
    ('La.', ('Louisiana',)),
    ('M.P.', ('Northern Mariana Islands',)),
    ('ME', ('Maine',)),
    ('Me.', ('Maine',)),
    ('MA', ('Massachusetts',)),
    ('Mass.', ('Massachusetts',)),
    ('MH', ('Marshall Islands',)),
    ('MD', ('Maryland',)),
    ('Md.', ('Maryland',)),
    ('MI', ('Michigan', 'Mississippi',)),
    ('MC', ('Michigan',)),
    ('Mich.', ('Michigan',)),
    ('MN', ('Minnesota',)),
    ('Mn.', ('Minnesota',)),
    ('Minn.', ('Minnesota',)),
    ('Miss.', ('Mississippi',)),
    ('MS', ('Massachusetts', 'Mississippi',)),
    ('MO', ('Missouri',)),
    ('Mo.', ('Missouri',)),
    ('MP', ('Commonwealth of the Northern Mariana Islands', 'Northern Mariana Islands',)),
    ('MT', ('Montana',)),
    ('Mont.', ('Montana',)),
    ('NB', ('Nebraska',)),
    ('NE', ('Nebraska',)),
    ('Neb.', ('Nebraska',)),
    ('Nebr.', ('Nebraska',)),
    ('NV', ('Nevada',)),
    ('Nv.', ('Nevada',)),
    ('Nev.', ('Nevada',)),
    ('NC', ('North Carolina',)),
    ('N.C.', ('North Carolina',)),
    ('N. Car.', ('North Carolina',)),
    ('N. Dak.', ('North Dakota',)),
    ('ND', ('North Dakota',)),
    ('N.D.', ('North Dakota',)),
    ('NH', ('New Hampshire',)),
    ('N.H.', ('New Hampshire',)),
    ('NJ', ('New Jersey', 'New Jersey (NJ)')),
    ('N.J.', ('New Jersey',)),
    ('NM', ('New Mexico',)),
    ('N.M.', ('New Mexico',)),
    ('N. Mex.', ('New Mexico',)),
    ('New M.', ('New Mexico',)),
    ('NY', ('New York',)),
    ('N.Y.', ('New York',)),
    ('N. York', ('New York',)),
    ('OH', ('Ohio',)),
    ('Oh.', ('Ohio',)),
    ('O.', ('Ohio',)),
    ('OK', ('Oklahoma',)),
    ('Ok.', ('Oklahoma',)),
    ('Okla.', ('Oklahoma',)),
    ('OR', ('Oregon',)),
    ('Or.', ('Oregon',)),
    ('Ore.', ('Oregon',)),
    ('Oreg.', ('Oregon',)),
    ('PA', ('Pennsylvania',)),
    ('Pa.', ('Pennsylvania',)),
    ('Penn.', ('Pennsylvania',)),
    ('Penna.', ('Pennsylvania',)),
    ('PI', ('Philippine Islands',)),
    ('PR', ('Puerto Rico',)),
    ('P.R.', ('Puerto Rico',)),
    ('PW', ('Palau',)),
    ('RI', ('Rhode Island',)),
    ('R.I.', ('Rhode Island',)),
    ('P.P.', ('Rhode Island',)),
    ('SC', ('South Carolina',)),
    ('S.C.', ('South Carolina',)),
    ('S. Car.', ('South Carolina',)),
    ('SD', ('South Dakota',)),
    ('S. Dak.', ('South Dakota',)),
    ('S.D.', ('South Dakota',)),
    ('Sodak', ('South Dakota',)),
    ('TN', ('Tennessee',)),
    ('Tenn.', ('Tennessee',)),
    ('Tn.', ('Tennessee',)),
    ('TX', ('Texas',)),
    ('Tex.', ('Texas',)),
    ('TT', ('Trust Territory of the Pacific Islands',)),
    ('U.S.V.I.', ('Virgin Islands',)),
    ('UM', ('U.S. Minor Outlying Islands',)),
    ('UT', ('Utah',)),
    ('Ut.', ('Utah',)),
    ('VI', ('Virgin Islands',)),
    ('V.I.', ('Virgin Islands',)),
    ('VA', ('Virginia',)),
    ('Va.', ('Virginia',)),
    ('Virg.', ('Virginia',)),
    ('VT', ('Vermont',)),
    ('Vt.', ('Vermont',)),
    ('WN', ('Washington',)),
    ('Wn.', ('Washington',)),
    ('WV', ('West Virginia',)),
    ('W.V.', ('West Virginia',)),
    ('W. Va.', ('West Virginia',)),
    ('W. Virg.', ('West Virginia',)),
    ('W.Va.', ('West Virginia',)),
    ('WA', ('Washington',)),
    ('Wa.', ('Washington',)),
    ('Wash.', ('Washington',)),
    ('Wash., D.C.', ('District of Columbia',)),
    ('WI', ('Wisconsin',)),
    ('Wi.', ('Wisconsin',)),
    ('Wis.', ('Wisconsin',)),
    ('Wisc.', ('Wisconsin',)),
    ('WS', ('Wisconsin',)),
    ('WY', ('Wyoming',)),
    ('Wy.', ('Wyoming',)),
    ('Wyo.', ('Wyoming',)),
]

def _find_entry(s):
    def _flatter(s):
        return s.lower().replace(' ', '').strip()

    if s is None:
        return None, None

    check_str = _flatter(s)
    
    for tup in STATE_MAP:
        k = tup[0]
        values = tup[1]

        if check_str == _flatter(k):
            return k, values[0]

        for v in values:
            if check_str == _flatter(v):
                return k, v

    return None, None

def us_state_name(s):
    """
    >>> us_state_name('TX')
    'Texas'

    >>> us_state_name('Texas')
    'Texas'

    >>> us_state_name('texas')
    'Texas'

    >>> us_state_name('MS')
    'Massachusetts'

    >>> us_state_name('MP')
    'Commonwealth of the Northern Mariana Islands'

    >>> us_state_name('oh hai')

    >>> us_state_name(None)
    
    >>> us_state_name('PA')
    'Pennsylvania'

    >>> us_state_name('RI')
    'Rhode Island'

    """
    matching_abbr, matching_name = _find_entry(s)

    return matching_name
    
def us_state_abbr(s):
    """
    >>> us_state_abbr('Texas')
    'TX'

    >>> us_state_abbr('TEXAS')
    'TX'

    >>> us_state_abbr('texas')
    'TX'

    >>> us_state_abbr('tx')
    'TX'

    >>> us_state_abbr('wisconsin')
    'WI'

    >>> us_state_abbr('Northern Mariana Islands')
    'CM'

    >>> us_state_abbr('oh hai!')

    >>> us_state_abbr(None)

    >>> us_state_abbr('Pennsylvania')
    'PA'

    >>> us_state_abbr('Rhode Island')
    'RI'

    """
    matching_abbr, matching_name = _find_entry(s)

    return matching_abbr

#--------------------------------------------------
#               MAIN
# --------------------------------------------------
if __name__ == "__main__":
    import doctest

    print('[abbr.py] Testing...')

    doctest.testmod()

    print('Done.')

