# To recreate
* Channels: run Python files without arguments
* Ca2+ diffusion: with NEURON:
```
cd diffusion
nrnivmodl
nrngui cadif.hoc
```

# Potassium DR channel (kdr)

* Graham 2014 Ka conductance for channel located on 50 um from soma:
![Graham 2014 Ka 50um](images/simulation/graham_ka_conductance_50um.png)

* Graham 2014 Ka conductance for channel located on 350 um from soma:
![Graham 2014 Ka 350um](images/simulation/graham_ka_conductance_350um.png)

* Graham 2014 Kdr conductance:
![Graham 2014 Kdr](images/simulation/graham_kdr_conductance.png)

* Graham 2014 Ka full characteristics:
![Graham 2014 Ka characteristics](images/simulation/graham_ka_characteristics.png)

* Graham 2014 Kdr full characteristics:
![Graham 2014 Kdr characteristics](images/simulation/graham_kdr_characteristics.png)

* HH K conductance
![HH K](images/simulation/hh_k_conductance.png)

* HH K open/close state from the book
![HH K open/close](images/book/kdrl_open.jpg)

* HH K conductance from the book for 26, 38, 63, 88, 109 mV
![HH K conductancy](images/book/kdr_conductancy.jpg)

* Simulational K open/close dynamics with alpha and beta params:
![SimulationalK open/close](images/simulation/kdr_open_close_sim.png)

* Open/close Book dynamics for alpha and beta params:
![HH K open/close](images/book/open_close_alpha_beta.jpg)

* HH Na conductance
![HH Na conductance](images/simulation/hh_na_conductance.png)

* HH Na conductancy from the book:
![Simulational Na conductancy](images/book/na_condictancy.jpg)

* Ca2+ dendritic diffusion (NEURON):
  * injection of 0.01 mM Ca2+ to the outermost shell compartment 0.0
  * simulation for 0.02 ms
  
![Ca2+_dendritic_diffusion](images/simulation/ca2_diffusion_with_xaxis.png)

* Ca2+ radial diffusion schema - spine_head->spine_neck->dendrite:

![Ca2+_spine_dendritic_diffusion](images/simulation/ca2+_radial_diffusion.png)

* Ca2+ for only dendritic spine head radial diffusion (NEURON):
  * injection of 0.01 mM Ca2+ to the 0.5 location on the head
  * simulation for 0.16 ms
  
![Ca2+_spine_dendritic_diffusion](images/simulation/ca2_radial_head_dif.gif)

* Ca2+ diffusion comparision of MOD-based shell diffusion vs RxD diffusion:

![ca2_diffusion_with_mod_and_rxd](images/simulation/ca2_diffusion_with_mod_and_rxd.png)

Book model of dendritic shells: Nicholas T. Carnevale, Michael L. Hines, The NEURON Book, 2006

Book photos of charts from: Sterratt, Graham et al. Principles of Computational Modeling in Neuroscience, 2011

