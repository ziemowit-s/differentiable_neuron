
TITLE Calcium ion accumulation with longitudinal and radial diffusion

NEURON {
	SUFFIX cadifusrect
	USEION ca READ cai, ica WRITE cai
	GLOBAL TotalBuffer
	RANGE cai0
	THREADSAFE
}

DEFINE NANN  4

UNITS {
	(molar) =	(1/liter)
	(mM) =	(millimolar)
	(um) =	(micron)
	(mA) =	(milliamp)
	FARADAY =	(faraday)	(10000 coulomb)
	PI = (pi)	(1)
}

PARAMETER {
    L (um)
	DCa = 0.6			(um2/ms) : diffusion coeficient
	: to change rate of buffering without disturbing equilibrium
	: multiply the following two by the same factor
	k1buf	= 100			(/mM-ms)
	k2buf	= 0.1			(/ms)
	TotalBuffer = 0.003	(mM)
	cai0 = 50e-6 (mM)	: Requires explicit use in INITIAL block
}

ASSIGNED {
    diam (um)
	ica		(mA/cm2)
	cai		(mM)
	Kd		(/mM)
	B0		(mM)
}

STATE {
	ca[NANN]		(mM) <1e-6>	: ca[0] is equivalent to cai
	CaBuffer[NANN]	(mM)
	Buffer[NANN]	(mM)
}

BREAKPOINT {
	SOLVE state METHOD sparse
}

LOCAL factors_done
LOCAL frat
LOCAL da

INITIAL {
	MUTEXLOCK
	if (factors_done == 0) {
		factors_done = 1
		da = diam/(NANN-1)
        frat = L/da : area_of_diffusion/thickness_of_the_shell
	}
	MUTEXUNLOCK

	cai = cai0
	Kd = k1buf/k2buf
	B0 = TotalBuffer/(1 + Kd*cai)

	FROM i=0 TO NANN-1 {
		ca[i] = cai
		Buffer[i] = B0
		CaBuffer[i] = TotalBuffer - B0
	}
}

KINETIC state {
	COMPARTMENT i, da*L {ca CaBuffer Buffer} : COMPARTMENT index, volume[index] {state1, state2}
	LONGITUDINAL_DIFFUSION i, DCa*da*L {ca}

	~ ca[0] << ((-ica*da*L)/(2*FARADAY))

	FROM i=0 TO NANN-2 { : radial diffusion
		~ ca[i] <-> ca[i+1] (DCa*frat, DCa*frat)
	}

	FROM i=0 TO NANN-1 { : calcium buffering
		~ ca[i] + Buffer[i] <-> CaBuffer[i] (k1buf*da*L, k2buf*da*L)
	}

	cai = ca[0]
}
