# Physics-informed neural networks for inverse problems in nano-optics and metamaterials (Chen, Lu, Karniadakis & Dal Negro, 2020)

> Fuente: `Chen_Lu_Karniadakis_DalNegro_2020_NanoOpticsMetamaterials.pdf` (convertido con pdftotext desde `master_supporting_docs/supporting_papers/referencias/`)

---

arXiv:1912.01085v2 [physics.comp-ph] 17 Mar 2020

Physics-informed neural networks for inverse problems in nano-optics and metamaterials
Yuyao Chen,1 Lu Lu,2 George Em Karniadakis,2 and Luca Dal Negro1, 2, 3, 4,  1Department of Electrical & Computer Engineering and Photonics Center, Boston University, 8 Saint Mary's Street, Boston, MA 02215, USA. 2Division of Applied Mathematics, Brown University, 170 Hope Street, Providence, Rhode Island, 02912, USA. 3Division of Material Science and Engineering, Boston University, 15 Saint Mary's Street, Brookline, MA 02446, USA. 4Department of Physics, Boston University, 590 Commonwealth Avenue, Boston, MA 02215, USA.
Abstract
In this paper we employ the emerging paradigm of physics-informed neural networks (PINNs) for the solution of representative inverse scattering problems in photonic metamaterials and nanooptics technologies. In particular, we successfully apply mesh-free PINNs to the difficult task of retrieving the effective permittivity parameters of a number of finite-size scattering systems that involve many interacting nanostructures as well as multi-component nanoparticles. Our methodology is fully validated by numerical simulations based on the Finite Element Method (FEM). The development of physics-informed deep learning techniques for inverse scattering can enable the design of novel functional nanostructures and significantly broaden the design space of metamaterials by naturally accounting for radiation and finite-size effects beyond the limitations of traditional effective medium theories.
 dalnegro@bu.edu
1

I. INTRODUCTION
For over two centuries, the science and engineering of electromagnetic waves in optical materials relied on either analytical solutions or numerical approximations of differential equations derived from physical models. While enormously successful, this approach fails to capture the multi-scale behavior of heterogeneous media whose structural complexity prevents the precise formulation and hence the solution of the high-frequency inverse scattering problem, which has numerous applications to optics, acoustics, geophysics, astronomy, medical imaging, microscopy, remote sensing, and nondestructive testing. This problem consists of determining the characteristics of an object from a limited set of measured data on how it scatters incoming radiation; solving this may enable the predictive design of artificial optical materials, i.e. metamaterials and complex optical nanostructures, starting directly from desired optical functionalities within a prescribed frequency range. However, in the presence of strong multiple light scattering the inversion of the physics-driven differential models of light scattering in complex multi-particle geometries becomes an intrinsically ill-posed problem. Under these circumstances, traditional numerical techniques fail to predict desired systems' parameters. In addition, optical nonlinearities and unavoidable noise render object reconstruction from available data a computationally intractable problem. These fundamental challenges motivated the development of alternative and more powerful computational frameworks that leverage sophisticated optimization methods for the solution of inverse scattering problems deep in the multiple scattering regime [1­6]. Very recently, the growing interest for machine learning algorithmic development in wave engineering led to successful applications to inverse scattering problems in imaging and tomography [7, 8], demonstrating the potential to open new territories with respect to medical imaging, microscopy, and remote sensing technologies.
Physics-informed neural networks (PINNs) [9, 10] is a general framework developed recently for solving both forward and inverse problems of partial differential equations. In this paper we propose and develop PINNs for the solution of different inverse scattering electromagnetic problems of direct interest to nano-optics and metamaterials technologies. In particular, we address the difficult problems of effective medium determination and parameter retrieval by applying the powerful PINNs framework to finite-size clusters of scattering nanocylinders arranged in periodic and aperiodic geometries. Moreover, using PINNs we
2

demonstrate the ability to efficiently reconstruct the spatial distribution of the electric permittivity of unknown objects from synthetic scattering data. Finally, we apply our method to the determination of the optimal dielectric permittivity of optical cloaking layers beyond the quasi-static limit. All our results are validated using numerical simulations based on the Finite Element Method (FEM) in two spatial dimensions.
Our work provides a novel and powerful framework for the inverse design of scattering nanostructures and photonic metamaterials based on the inversion of their scattered fields. Moreover, this ability establishes remote sensing functionalities in the optical regime whereby the unknown dielectric permittivity of complex optical nanostructures can be unambiguously retrieved from near-field optical imaging data.
II. PHYSICS-INFORMED NEURAL NETWORKS
Our approach leverages the capabilities of deep neural networks as universal function approximators. However, differently from standard deep learning approaches, PINNs restrict the space of admissible solutions by enforcing the validity of partial differential equation (PDE) models governing the actual physics of the problem. This is achieved within relatively simple feed-forward neural network architectures leveraging automatic differentiation (AD) techniques readily available in the TensorFlow learning package [11]. Moreover, PINNs use only one training dataset to achieve the desired solutions, thus relaxing the burdens often imposed by the massive training datasets necessary in alternative, i.e. non physicsconstrained, deep learning approaches. Moreover, PINNs do not require any data on the inverse parameters it predicts, and thus it belongs to unsupervised learning. These unique features of PINNs are greatly beneficial for the solution of inverse scattering problems either with measured field data or with synthetic ones generated by forward simulations. Importantly, PINNs solve highly-nonlinear and dispersive inverse problems on the same footing as forward problems, by the simple addition of an extra loss term to the overall loss function for the minimization of the residuals of PDEs and their boundary conditions [9]. Therefore, PINNs are particularly effective in solving ill-posed inverse problems, which are often intractable with available mathematical formulations.
In this section, we introduce the algorithm for solving inverse PDE models with PINNs. The main idea of PINNs is schematically illustrated in Fig. 1 (a). We first construct a neural
3

FIG. 1. (a) Schematic of a PINN for solving inverse problem in photonics based on partial differ-

ential equations. The left part neural network represents a surrogate model u of the PDE solution.

The right part shows the loss function to restrict u to satisfy PDE in the domain , boundary

conditions (BC) u^(x, y) = gD(x, y) on D

 , and

u^ n

(x,

y)

=

gD(u, x, y)

on

R



.

The

initial condition (IC) is treated as a special type of boundary conditions. For inverse problem, we

have also loss term from u^ - u on residual points. We optimize the neural network's weights and

biases to obtain loss smaller than . (b) The process shows the process of PINNs to reconstruct

the permittivity profile  from a known scattering field profile dataset.

network with the output u^(x; ) as a surrogate of the PDE solution u(x). Here, we employ the feed-forward neural network (FNN), which is relatively simple but sufficient for most PDE problems, and  is a vector containing all weights and biases in the neural network that needs to be trained. Then, the next key step is to constrain the neural network's output u^ to satisfy the PDE as well as data observations u. This is realized by constructing the loss function by considering terms corresponding to PDE, boundary conditions and initial conditions, and the field observations. Specifically, we consider the following PDE problem with unknown parameter  for the solution u(x) with x = x1, . . . , xd defined on a domain
4

  Rd:

u^

u^ 2u^

2u^

f x; , . . . , ;

,...,

; . . . ;  = 0, x  .

(1)

x1

xd x1x1

x1xd

We denote Ti   be the points where we have the PDE solution u(x). The loss function is

then defined as:

L(, ) = wf Lf (, ; Tf ) + wiLi(, ; Ti) + wbLb(, ; Tb),

(2)

where:

1

u^

u^ 2u^

2u^

2

Lf (, ; Tf ) = |Tf | xTf f

x; , . . . , ;

,...,

;...;

x1

xd x1x1

x1xd

,
2

(3)

1 Li(, ; Ti) = |Ti| xTi

u^(x) - u(x)

2 2

,

(4)

1 Lb (, ; Tb) = |Tb| xTb

B(u^, x)

2 2

,

(5)

and wf , wb, and wi are the weights. Tf , Ti, Tb denote the residual points from partial differential equations, training dataset, and ICs and BCs, respectively. Here, Tf   is a set of predefined points to measure the matching degree of the neural network output u^ to the

PDE. Tf can be chosen as grid points or random points, see more details and discussion in reference [10]. In the last step, we optimize  and  by minimizing the loss function L(, ).

Note that using PINNs the only difference between a forward and an inverse problem is the

addition of an extra loss term Li to Eq. 2, which comes at an insignificant computational cost. We use DeepXDE [10], a user-friendly Python library, for the code implementation in

this paper.

III. PINNS FOR THE HOMOGENIZATION OF FINITE-SIZE METAMATERIALS
Photonic metamaterials are artificial structures composed of designed subwavelength building blocks that can achieve unusual optical properties [12]. The current underpinning of metamaterials design relies on the effective medium theory (EMT) [13­15], which is actively investigated in electromagnetic research from different perspectives such as the methods of coherent potential approximation (CPA) [16, 17], the multipole expansion method [18], or the field averaging procedure [19] are used to homogenize metamaterials properties. Here
5

we propose to use PINNs for the homogenization of dielectric metamaterials formulated as an inverse medium problem for finite-size systems. Specifically, we set up large clusters composed of several hundreds dielectric nanocylinders arranged in periodic and aperiodic geometries and demonstrate, using PINNs, direct retrieval of the effective permittivity distribution that gives rise to the same scattered field as the original cluster. We refer to this approach as "inverse metamaterials design".
In order to achieve our goals we constrained PINNs using the Helmholtz equation for weakly inhomogeneous two-dimensional (2D) media under TM polarization excitation:

2Ez (x, y) + r (x, y) k02Ez = 0,

(6)

where Ez is the electric field z component, r(x, y) is the space dependent relative permittiv-

ity,

and

k0

=

2 0

is

the

wavenumber

in

free

space.

We

first

consider

dielectric

materials

with

real permittivity values and ignore the radiation losses in the effective medium, which will be

addressed later in this section. However, as discussed at the end of the section, our method

can be easily generalized to include lossy component materials as well. As schematically il-

lustrated in Fig. 1(b), the problem at hand is the one to retrieve the function (x, y), which

corresponds to the unknown parameters  in Fig. 1(a), by training PINNs on synthetic data

obtained via the forward solution u(x, y) of the scattering problem using FEM. Validation

of the permittivity spatial profile predicted by PINNs is obtained using the retrieved (x, y)

within a forward scattering FEM simulation. The resulting electric field distribution is then

compared to the one of the original forward FEM simulation used to generate the training

(synthetic) scattering data. The discrepancy between these two datasets is quantified by

computing the L2 error norm of the corresponding total field distributions. It is important

to realize that in this section we train PINNs to predict the permittivity profile across the

entire computational domain and therefore in this case we do not need to explicitly consider

the loss term for the boundary conditions Tb.

We show in Fig. 2 (a) the representative schematics of a square lattice structure used for

inverse metamaterial design, where a denotes the center-to-center distance of the nanocylin-

ders in the array, and r is radius of each nanocylinder. The array pattern is truncated using

a circular window with diameter d. Fig. 2 (b) illustrates the real part of the computed

electric field distribution Ez using FEM for a square lattice with parameters: a = 500nm, r = 125nm, d = 10µm, number of particles N = 317, and permittivity of nanocylinder

6

FIG. 2. (a) FEM simulation of electric field real part distribution profile for square lattice arranged scatters with a = 500nm, r = 125nm, d = 10µm, N = 317, = 3. The illumination plane wave wavelength is  = 2.1µm. (b) depicts the inverse train dataset for training PINNs to homogenize from panel (a). (c) shows the PINNs predicted permittivity profile by training with dataset shown in panel (b). (d) illustrates the FEM validation of electric field distribution when illuminating plane wave with wavelength  on the object with PINNs predicted permittivity profile. The L2 error between the panel (b) and (d) is 2.82%.
 = 3. The array is illuminated by a plane wave with wavelength  = 2.1µm. In the forward FEM simulation we used a minimum element size of 0.6 nm with Perfectly Matching Layer (PML) boundary with 3µm thickness, resulting in 2742129 total degrees of freedom. We used the electric field data shown in Fig. 2 (b) as the synthetic train dataset for PINNs. In all simulations we sampled the electric field using a 150 × 150 spatial resolution. The utilized PINN architecture is composed of a feed-forward neural networks with 4 hidden layers and 64 neurons in each hidden layers. We used the hyperbolic tangent activation function and chose the Glorot uniform method for the weight initialization. The learning rate for the training was set to 10-3. Finally, we train the neural networks using the Adam methods and train for 150000 iterations (epochs) before reaching a satisfactory loss value of 10-2. The
7

predicted (x, y) profile obtained by this PINN is shown in Fig. 2 (c). We note that for the considered parameters of the scattering array PINN retrieves the permittivity distribution of a single dielectric nanocylinder with an effective dielectric function. Therefore, training PINNs to predict the permittivity distribution of the finite-size cluster of scattering cylinders that yield the same field distribution of the forward FEM scattering calculation has resulted in the effective homogenization of a finite-size metamaterial. Since we are working here under the conditions of small size parameter for the nanocylinders (r, a << ) and weak scattering ( = 3), we can also estimate the effective medium permittivity using the classical Bruggeman mixing formula [15]:

i

fi

i i

- e + e

=

0,

(7)

where e is the effective permittivity, fi and i are the filling fraction and permittivity of each component, respectively. By using Eq. 7, we predicted e = 1.25. The epsilon distribution (x, y) from PINNs averaged inside the cylindrical windowed region (r < 5µm)

is 1.35 ± 0.056. The permittivity error between the PINN prediction and the Bruggeman

model is 7%. Therefore, the value computed by the Bruggeman mixing formula in the weak

scattering regime is compatible with the one predicted using PINNs. A direct validation of

the PINN results is obtained by directly employing the  profile estimated by PINN and

shown in Fig. 2 (c) inside forward scattering FEM simulations. The FEM computed total

field Ez distribution considering the PINN-predicted  under the same excitation conditions is shown in Fig. 2 (d). We further calculated the L2 error norm between Fig. 2 (b) and (d).

This error is 2.82%, indicating a very good retrieval of the permittivity profile using PINNs.

To further study the role on the homogenization of the radiation effects introduced by the cylindrical scatterers we increased the permittivity of each nanocylinder in the array by considering  = 12. Fig. 3 (a) illustrates the real part of the total electric field distribution obtained from the plane wave excitation of such an array using FEM simulations with the same parameters as for the case in Fig. 2. However, in the present case we observe a strong perturbation of the electric field around the array indicating the presence of stronger scattering effects. Using the same parameters and training method as in the previous case, PINN predicts now the permittivity profile displayed in Fig. 3 (b). Differently from the results previously shown in Fig. 2 (c), now PINN retrieves a non-homogeneous effective
8

FIG. 3. (a) depicts the training dataset for the PINNs from FEM simulation of electric field real part distribution profile for square periodically arranged scatters with a = 500nm, r = 125nm, d = 10µm, N = 317,  = 12. The illumination plane wave wavelength is  = 2.1µm. (b) shows the PINNs predicted inverse permittivity profile by training with dataset shown in panel (a). (c) illustrates the FEM validation of electric field distribution when illuminating plane wave with wavelength  on the object with PINNs predicted permittivity profile.

medium that contains a spatial region of negative effective permittivity. We implemented

this permittivity profile in the FEM simulation and obtained the electric field distribution

shown in Fig. 3 (c). The quality of the PINN prediction is again quantified by considering

the L2 error norm between data in Fig. 3 (a) and (c), which is now 5%. Our findings

indicate that PINNs effectively account for scattering and radiation effects in the array by

retrieving a non-homogeneous effective medium with resonant permittivity profile, beyond

the capabilities of traditional effective medium theory.

The proposed PINNs framework for metamaterial inverse design is not limited by the

periodic arrangement of the scattering nanocylinders in the array. In fact, the exact same

procedure can be utilized for the synthesis of non-homogeneous effective media correspond-

ing to scattering arrays with arbitrary aperiodic morphology. In order to prove this point

we consider next the case of a Vogel spiral array. Vogel spirals have been intensively inves-

tigated in plasmonics and nanophotonics literature thanks to their unique light scattering

and localization properties that stimulated novel device applications [20­27]. Vogel spirals

are defined in polar coordinates by following parametric equations:





rn = a0 n

(8)

n = n

9

FIG. 4. FEM simulation of electric field real part distribution profile for Vogel spiral arranged scatters. The illumination plane wave wavelength is  = 2.1µm. (b) depicts the inverse train dataset for training PINNs homogenization from panel (a). (c) shows PINNs predicted inverse permittivity profile by training with dataset shown in panel (b). (d) illustrates the FEM validation of electric field distribution when illuminating plane wave with wavelength  on the object with PINNs predicted permittivity profile. The L2 error between the panel (b) and (d) is 3.8%.
where n = 0, 1, 2, ... is an integer, a0 is a positive constant called scaling factor, and  is an irrational number, known as the divergence angle[28]. This angle specifies the constant aperture between successive point particles in the array. Since the divergence angle is an irrational number, Vogel spiral point patterns lack both translational and rotational symmetry.
Here we studied PINNs homogenization of a Vogel spiral array in the radiative (scattering) limit. The Vogel spiral pattern considered here is shown in Fig. 4 (a) and is characterized by an averaged center-to-center interparticle distance a¯ = 500nm, d = 10µm, r = 125nm,  = 12, and N = 300. The corresponding total electric field distribution computed with FEM under plane wave excitation with  = 2.1µm is shown in Fig. 4 (b). We can appreciate immediately the asymmetric distribution of the total field around the Vogel spiral array and also the strong perturbation of the field due to the strong scattering effects of the
10

nanocylinder. By training with the same network parameters established in previous case, PINN now predicts the effective permittivity distribution (x, y) illustrated in Fig. 4 (c).

We note that the  profile recovered from PINN is asymmetric, which results from the asymmetric nature of the Vogel spiral structure. It also contains a negative permittivity

region that effectively accounts for the strong radiation effects in the Vogel array. Finally, we show in Fig. 4 (d) the electric field distribution obtained from FEM forward simulations by using as an input the effective permittivity profile obtained from PINN. The L2 error norm between the total electric fields shown in Fig. 4 (b) and (d) is found to be 3.8%.

The proposed method can naturally be generalized to account for radiation losses in the multiple scattering medium by retrieving the complex permittivity of the effective medium. In this case we need to consider Eq. 6 with both Ez and r(x, y) as complex variables. Separating real and imaginary parts, we then obtain the following PDE model for PINNs:



2Re{Ez} (x, y) + [Re{Ez}Re{r (x, y)} - Im{Ez}Im{r (x, y)}] k02 = 0

(9)

2Im{Ez} (x, y) + [Im{Ez}Re{r (x, y)} + Re{Ez}Im{r (x, y)}] k02 = 0

where Re{·} and Im{·} denote the real and imaginary parts of the corresponding quantities. We can now train PINNs using both the real and the imaginary parts of Ez computed from the FEM simulations. This will enable PINNs to predict independently Re{r (x, y)} and Im{r (x, y)} for the effective medium and therefore to quantify its radiation losses. We have implemented this more general model using the same neural network parameters and training method described in the previous cases and we have applied them to the structure shown in Fig. 2-4 in order to predict Im{r (x, y)} for the respective effective media. The maximum values of Im{r (x, y)} obtained in these three cases are 10-4, 0.6, and 0.3, respectively. Finally we notice that the real parts Re{r (x, y)} of the predicted complex permittivity remain very close, within a total 3% error, to the values previously obtained considering only the real part of the effective medium. However, the more general approach outlined above allows one to investigate arrays of nanocylinders with even larger refractive index contrast where radiation losses, which are difficult to account using traditional effective index theory [15], are expected to play a very important role.
Therefore, our results demonstrate that the general PINNs framework is suitable to systematically study the effects of morphology and radiation coupling in arbitrary non-periodic effective media and metamaterials, beyond the limitations of effective medium theory. The

11

ability to reliably identify the effective media that yield the same total field as arbitrary scattering arrays using PINNs can not only greatly stimulate the development of novel finite-size metamaterials and resonant nanostructures but also provides fundamental insights to advance the current status of advanced homogenization theory with radiation effects [29, 30].

IV. PINN FOR INVERSE MIE SCATTERING

We showed in previous section that PINNs are capable of homogenizing arrays composed

of sub-wavelength particles arranged in arbitrary aperiodic geometries. In this section we

will further show that, based on the knowledge of the field values around compound optical

nanostructures of known morphology, PINNs can successfully retrieve their optical parame-

ters. This specific application requires the solution of an inverse problem with a PINN that,

differently from the previous sections, includes the specific boundary conditions in the def-

inition of the appropriate PDE model. The results shown in this section demonstrate that

PINNs framework can potentially be applied to retrieve the optical properties of complex

nanostructures from near-field imaging data [31].

We start our analysis by considering the case of retrieving the permittivity of a single

resonant nanocylinder from its external total field. We compute the external electric field

distribution, shown in Fig. 5 (a), using the analytical Mie scattering theory [32] for a

cylinder with radius r = 2µm and permittivity  = 4 under TM wave excitation at a

wavelength  = 3µm. Note that the field inside the cylinder is not specified here. In order

to retrieve the internal field distribution along with the unknown permittivity parameter of

the nanocylinder, we implemented the following PDE model:



2Ez(k) + rkk02Ez(k) = 0 in k, (k = 1, 2)







Ez(1)

= Ez(2)



r=a

r=a



 1 Ez(1)  = µr1 r r=a

1 Ez(2) µr2 r r=a

(10)

where Ez(1), Ez(2) denotes the electric field z component real part inside and outside the

nanocylinder, respectively. Here r denotes the radial components in cylindrical coordinates

while a is the nanocylinder radius. r1, r2 are the relative permittivity of the nanocylinder and the host medium, respectively. µr1, µr2 are the relative permeability of the corresponding regions. We are considering non-magnetic materials in this section so we have µr1 = µr2 = 1.

12

Moreover, we set r2 = 1 while r1 is a trainable variable that PINNs retrieve through the training process fed by the analytically computed external field.
FIG. 5. (a) shows the train dataset for inverse Mie scattering theory by using PINNs; we used only the external electric field distribution with the nanocylinder radius r = 2µm, r2 = 4, incident wavelength  = 3µm, (b) shows PINNs inverse finding of the nanocylinder permittivity as a function of iteration step, (c) shows the reconstructed electric field distribution for the nanocylinder scattering from PINNs, (d) illustrates the real electric field distribution of the given nanocylinder using Mie theory. The L2 error between the panel (c) and (d) is 0.51%.
The same network architecture and hyperparameters as in the previous training cases are utilized here. However, we multiplied the loss term Ti by a factor 100 in order to enforce a stronger penalty and obtain better train results. We stop training after 105 steps that we found sufficient to achieve a 10-4 train loss value. The retrieval of r2 during the training process is illustrated in Fig. 5 (b), where the dashed line indicates the true solution from analytical Mie theory. We can see clearly that PINNs successfully retrieve the true solution when fed with only information on the external field. Furthermore, the reconstructed field from PINNs, displayed in Fig. 5 (c), shows a very small difference from the Mie theory (Fig. 5 (d)) that is quantified by an L2 error norm of 0.51%. Therefore, we show that PINNs can
13

successfully retrieve both the internal field and the cylinder permittivity when constrained by a physical PDE model.

FIG. 6. (a) shows the schematic of the studied coated nanocylinder parameters, (b) shows reconstructed electric field distribution for the coated nanocylinder under the excitation of plane wave with  = 3µm, (c) illustrates the inverse finding of the two parameters i, c with respect to the number of iteration of PINN, (d) shows the reconstructed electric field distribution from PINNs after 104 training steps.

Furthermore, we now extend PINNs to the retrieval of multiple materials parameters by considering the case of a coated nanocylinder. The geometry of the studied coated nanocylinder is schematically illustrated in Fig. 6 (a). The spatial distribution of the real part of the total electric field of the coated nanocylinder with a = 0.5µm, b = 1µm, i = 3, c = 2 is shown in Fig. 6 (b). The corresponding PDE model that we implemented within PINNs framework to solve this inverse problem is reported below:



2Ez(k) 

+

k k02 Ez(k)

=

0

in k, (k = 1, 2, 3)





Ez(1)

= Ez(2)

, Ez(2)

= Ez(3)



r=a

r=a

r=b

r=b



  

1

 Ez(1)

 µi r

=
r=a

1 Ez(2) µc r

,
r=a

= 1 Ez(2)
µc r r=b

1 Ez(3) µ0 r r=b

(11)

14

where Ez(1), Ez(2), Ez(3) denote the z components of the real parts of the electric fields inside the inner core, coated layer, and outside coating layer, respectively. i, c, 0 are the relative permittivities of the inner-core, coated layer, and host medium, respectively. µi, µc, µ0 are the relative magnetic permeabilities of the corresponding regions that are here set equal to unity since we are considering non-magnetic materials. In the parameter retrieval process, we fix 0 = 1 and train PINNs to predict i and c based on the field distribution from Fig. 6 (b). Specifically, We utilize the same neural network architecture and training method as for the single nanocylinder case. Figure 6 (c) shows clearly the parameter retrieval during the training process, which converges to the exact values used to create the training data. Figure 6 (d) shows the reconstructed field. The L2 error norm between Fig. 6 (b) and (d) is only 1%. Therefore, we showed that PINNs can successfully retrieve multiple material parameters for compound resonant nanostructures uniquely based on the total field information surrounding the objects.
We show next that in addition to retrieving the optical parameters of individual nanostrucutres, PINNs can additionally extract the parameters in systems composed of multiple objects. Inspired from the scattering target FoamDielExtTM [33] frequently used in diffraction tomography at GHz frequencies [3, 4, 7], we study parameter retrieval in the setup shown in Fig. 7 (a). The real part of the total electric field distribution for the considered structure under incident plane wave illumination at wavelength  = 2.1µm is illustrated in Fig. 7 (b). Using this field as the train dataset, we couple PINNs with the PDE homogenization model in Eq.6 and directly retrieve the permittivity profile over the entire computational window that gives rise to the same total field as the asymmetric dimer in 7 (a). In order to improve the quality of the reconstruction here we utilize the ResNet architecture with two residual blocks and each residual block has two fully-connected layers with width 64. We used the same activation function and initialization strategy as in all previous simulations. We multiply again the loss term Ti by a factor 100 to obtain better train results. The training process uses the Adam optimizer and is stopped after 150000 iterations resulting in 10-4 training losses. The retrieved (x, y) profile from this PINN is shown in Fig. 7 (c). We observe that the PINN reconstructed two object permittivities localized within regions that qualitatively correspond to the input target. The electric field distribution obtained by FEM using the permittivity profile retrieved by PINN is illustrated in Fig. 7 (d), where the L2 error norm between these two field profiles is 0.3%. Notice that
15

FIG. 7. (a) shows the permittivity profile of the two asymmetric dimer with 0 = -2, 1 = -10, r0 = 2µm, r1 = 0.8µm, (b) depicts train dataset for PINN from FEM simulation of electric field distribution profile for the asymmetric dimer shown in (a). The incident electromagnetic wave wavelength is  = 2.1µm (c) shows the PINN predicted permittivity profile after train, (d) illustrates the FEM validation of the electric field distribution for predicted permittivity by PINN. The L2 error between the panel (b) and (d) is 0.30%.
in the PDE homogenization model used here there are no boundary conditions specified to constrain the PINN solution. As a result, PINN found an equivalent permittivity profile that gives rise to the same field distribution as the train dataset but this solution may not be unique. This is the reason why the retrieved permittivity distribution is quite different in this case from the input target, despite the two share the same scattering behavior within the considered window. In all cases, when the morphology of a scattering object is known or characterized experimentally, PINNs framework can be utilized to retrieve nanomaterial properties based on scattered fields that can, for instance, be measured from scanning near-field optical microscopy (SNOM) [34]. The ability to infer material properties directly from imaging data using PINNs can provide unique opportunities for remote sensing and detection in the optical regime.
16

V. PINN FOR INVISIBLE CLOAKING DESIGN

In this section, we will show how to reformulate the well-known invisible cloaking problem

into a general parameter retrieval problem that can be accurately solved using PINNs. The

cloaking problem has stimulated significant interest in recent years [35, 36], and admits

an analytical solution in the limit of small objects compared to the incoming wavelength

(quasi-static limit). The considered geometry is illustrated in Fig. 8 (a) and consists of

an inner nanocylinder with radius a and permittivity i coated by a cloaking material with thickness equals to b - a and unknown permittivity c that cancels the scattering for a given plane wave incidence condition. We chose the following parameters for our cloaking

example: a = 0.12µm, b = 0.3µm, i = 4. Notice that for nanocylinders of small size

parameters (k0b << 1), we can obtain the permittivity of the cloaking layer c using the

following analytical formula [37]:

b =

c - i

(12)

a

c - 0

enabling verification of PINN-predicted results.

In order to generate the training data for PINNs we computed the electric field distribu-

tion of the coated nanocylinder using Mie theory with c that satisfies the cloaking Eq. 12. The obtained field distribution (excluding the internal field) is then used as the train dataset

for PINNs as illustrated in Fig. 8 (b). In this example we used the PDE model previously

defined by Eq. 11. We again employ a simple feed-forward neural network with 4 hidden

layers and 64 neurons in each hidden layers. Hyperbolic tangent activation function and

Glorot uniform initializer are used as in previous cases. However, here we utilized a learning rate for the training equal to 10-4. We trained the PINN neural networks with the Adam optimizer and considered 2 × 105 iteration steps, resulting in overall training losses equal to 10-4. In order to obtain better accuracy we multiply the loss term Ti as well as the loss term from the Ez continuity at interface r = b by a factor 100. We let the PINN retrieves both the electric permittivity and the magnetic permeability. The parameter retrieval curves as

a function of the iteration number are shown in Fig. 8 (c). These data demonstrate that

PINNs correctly find the true solution of the coating layer permittivity in complete agree-

ment with the analytical expression. Moreover, it is important to note that the considered

PINN obtains a magnetic (relative) permittivity equal to unity, confirming that no magnetic

response is necessary for perfect scattering cancellation in this geometry for a small particle

17

FIG. 8. (a) shows the schematic for nanocylinder with constant permittivity coated layer zeroing out scattering, a = 0.12µm, b = 0.3µm, i = 4, (b) shows the inverse train dataset for PINNs, the excitation plane wave wavelength  = 2.1µm, (c) illustrates PINNs predicted permittivity for the coating layer to zero out scattering. The dashed line is the analytical solution of the coating layer permittivity to zero out the nanocylinder scattering. (d) demonstrates the electric field distribution for coated nanocylinder with the coating layer permittivity predicted by PINN.
size. Fig. 8 (d) displays the reconstructed electric field from PINN, showing clearly that the electric field propagates the coated nanocylinder without any perturbation.
Finally, we address the conditions to achieve radiation cloaking in coated nanocylinders whose diameter equals the incoming wavelength. Although no perfect cloaking condition is theoretically expected in this case, it is still very interesting to use PINNs to discover the coating parameters for the optimal scattering reduction. The geometry of the problem is the same as in Fig. 8 (a) but here we additionally let the permittivity of the coating layer to be spatially dependent c(x, y) (within the layer) in order to obtain better cloaking results. Figure 9 (a) shows the training dataset for PINN under plane wave illumination with wavelength  = 2.1µm, and corresponds to a wave that propagates through the coated nanocylinder undisturbed. We emphasize that this situation cannot physically occur when the particle size is comparable to the wavelength. However, we will show that training under
18

FIG. 9. (a) shows the inverse train dataset for PINNs, where the excitation plane wave wavelength  = 2.1µm, (b) illustrates PINNs predicted permittivity distribution for the coating layer, (c) depicts the field distribution reconstructed from PINNs for the coated nanocylinder, (d), (e) show the electric field distribution for coated nanocylinder and without coating nanocylinder, respectively. (f) illustrates the normalized scattering cross section  spectrum for the nanocylinder with or without PINNs identified cloaking.
such a desirable condition allows PINNs to discover a permittivity profile that substantially reduces the scattering cross section of the cylinder.
We used the same PDE model as defined by Eq. 11 but we fixed the value to the magnetic permeability to unity in order to design a purely dielectric device. Given the complexity of this problem we modified the neural network architecture by considering 5 hidden layers while keeping all the other parameters as in previous cases. We additionally multiply the loss term Ti by a factor of 20 in order to obtain better training quality. The neural network is trained up to 2 × 105 steps and training loss values around 10-4 are achieved in the end.
Figures 9 (b) and (c) display the PINN-predicted c(x, y) distribution and the total field distribution. The PINN-predicted c(x, y) is then used in the FEM simulations resulting in the total electric field profile shown in Fig. 9 (d). For comparison, we also show the electric field distribution for the bare nanocylinder without the coating layer in Fig. 9 (e). It is clear that PINNs identified the dielectric properties of the coating layers that significantly reduce the far-field scattering of the device under plane wave excitation. Specifically, we quantified
19

this by computing the far-field scattering efficiency of the coated cylinder and confirmed a 75% reduction in the scattering efficiency due to the coating layer characteristics identified using PINNs, as shown in Fig. 9 (f). In summary, using the flexible PINNs framework we have established not only a powerful approach to retrieve material parameters based on scattering data (synthetic or measured) but also to design novel dielectric devices with strongly reduced scattering properties.
VI. CONCLUSIONS
We demonstrated in this paper the solution of representative inverse scattering problems that are particularly interesting in photonic metamaterials and nano-optics technologies. In particular, we successfully introduced and validated the PINNs framework for the effective medium reconstruction of scattering arrays where finite-size and radiation effect significantly perturb the classical homogenization picture. Our approach leverages recent advances in deep-learning algorithms constrained by the wave physics of the problems, which dramatically simplifies data training procedures compared to alternative machine learning approaches. Our findings have been fully validated using Finite Element Method (FEM) numerical simulations. In addition, we developed the PINNs framework for the retrieval of multiple optical parameters based on the field distribution around nanomaterials, which suggests a method to directly access material information from near-field imaging data. Finally, we use PINNs to address the problem of invisible cloaking with coated cylinders and show 75% scattering abatement in dielectric coated cylinders with size comparable to the wavelength of the incoming radiation. We believe that further PINNs development for inverse scattering and remote sensing of nanostructures can significantly broaden current design capabilities and also provide fundamental insights to advance the current state of homogenization theory with radiation effects. Although the PINNs architectures employed here are based on empirical tuning, recent advances in meta-learning [38­40] can enable future automated selection of the optimum architectures.
FUNDING
This research was sponsored by the Army Research Laboratory and was accomplished
20

under Cooperative Agreement Number W911NF-12-2-0023. The views and conclusions contained in this document are those of the authors and should not be interpreted as representing the official policies, either expressed or implied, of the Army Research Laboratory or the U.S. Government. The U.S. Government is authorized to reproduce and distribute reprints for Government purposes notwithstanding any copyright notation herein. This work was also supported by the DOE PhILMs project (No. de-sc0019453).
DISCLOSURES
The authors declare no conflict of interest.
ACKNOWLEDGMENTS
L. D. N. would like to thank Professors Nader Engheta and Salvatore Torquato for insightful discussions on non-homogeneous metamaterials and effective medium theory.
[1] Ulugbek S Kamilov, Ioannis N Papadopoulos, Morteza H Shoreh, Alexandre Goy, Cedric Vonesch, Michael Unser, and Demetri Psaltis, "Learning approach to optical tomography," Optica 2, 517­522 (2015).
[2] Sean Molesky, Zin Lin, Alexander Y Piggott, Weiliang Jin, Jelena Vuckovi´c, and Alejandro W Rodriguez, "Inverse design in nanophotonics," Nature Photonics 12, 659­670 (2018).
[3] Hsiouyuan Liu, Dehong Liu, Hassan Mansour, Petros T Boufounos, Laura Waller, and Ulugbek S Kamilov, "Seagle: Sparsity-driven image reconstruction under multiple scattering," IEEE Transactions on Computational Imaging 4, 73­86 (2017).
[4] Ulugbek S Kamilov, Hassan Mansour, and Brendt Wohlberg, "A plug-and-play priors approach for solving nonlinear imaging inverse problems," IEEE Signal Processing Letters 24, 1872­1876 (2017).
[5] Thanh-An Pham, Emmanuel Soubies, Alexandre Goy, Joowon Lim, Ferr´eol Soulez, Demetri Psaltis, and Michael Unser, "Versatile reconstruction framework for diffraction tomography with intensity measurements and multiple scattering," Optics Express 26, 2749­2763 (2018).
21

[6] David Colton and Rainer Kress, "Looking back on inverse scattering theory," SIAM Review 60, 779­807 (2018).
[7] Yu Sun, Zhihao Xia, and Ulugbek S Kamilov, "Efficient and accurate inversion of multiple scattering with deep learning," Optics Express 26, 14678­14688 (2018).
[8] Yash Sanghvi, Yaswanth Kalepu, and Uday K. Khankhoje, "Embedding deep learning in inverse scattering problems," IEEE Transactions on Computational Imaging (2019).
[9] M. Raissi, P. Perdikaris, and G. E. Karniadakis, "Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations," J. of Comp. Phys. 378, 686­707 (2019).
[10] Lu Lu, Xuhui Meng, Zhiping Mao, and George E Karniadakis, "Deepxde: A deep learning library for solving differential equations," arXiv preprint arXiv:1907.04502 (2019).
[11] M. Abadi, P. Barham, Z. Chen, A. Davis, J. Dean, S. Ghemawat, G. Irving, and M. Isard, "Tensorflow:a system for large-scale machine learning," 12th USENIX Symposiumon Operating Systems Design and Implementation , 265­283 (2016).
[12] Costas M Soukoulis and Martin Wegener, "Past achievements and future challenges in the development of three-dimensional photonic metamaterials," Nature Photonics 5, 523 (2011).
[13] Ping Sheng, Introduction to wave scattering, localization and mesoscopic phenomena, Vol. 88 (Springer Science & Business Media, 2006).
[14] Tuck C Choy, Effective medium theory: principles and applications, Vol. 165 (Oxford University, 2015).
[15] Ari H Sihvola, Electromagnetic mixing formulas and applications, 47 (The Institution of Engineering and Technology, 1999).
[16] Ying Wu, Jensen Li, Zhao-Qing Zhang, and CT Chan, "Effective medium theory for magnetodielectric composites: Beyond the long-wavelength limit," Physical Review B 74, 085111 (2006).
[17] Hao Zhang, Yongqiang Shen, Yuchen Xu, Heyuan Zhu, Ming Lei, Xiangchao Zhang, and Min Xu, "Effective medium theory for two-dimensional random media composed of core-shell cylinders," Optics Communications 306, 9­16 (2013).
[18] Ioannis Chremmos, Efthymios Kallos, Melpomeni Giamalaki, Vassilios Yannopapas, and Emmanuel Paspalakis, "Effective medium theory for two-dimensional non-magnetic metamaterial lattices up to quadrupole expansions," Journal of Optics 17, 075102 (2015).
22

[19] Victor V Gozhenko, Anthony K Amert, and Keith W Whites, "Homogenization of periodic metamaterials by field averaging over unit cell boundaries: use and limitations," New Journal of Physics 15, 043030 (2013).
[20] Jacob Trevino, Seng Fatt Liew, Heeso Noh, Hui Cao, and Luca Dal Negro, "Geometrical structure, multifractal spectra and localized optical modes of aperiodic vogel spirals," Optics Express 20, 3015­3033 (2012).
[21] Nate Lawrence, Jacob Trevino, and Luca Dal Negro, "Control of optical orbital angular momentum by vogel spiral arrays of metallic nanoparticles," Optics Letters 37, 5076­5078 (2012).
[22] Michael E Pollard and Gregory J Parker, "Low-contrast bandgaps of a planar parabolic spiral lattice," Optics Letters 34, 2805­2807 (2009).
[23] Jacob Trevino, Hui Cao, and Luca Dal Negro, "Circularly symmetric light scattering from nanoplasmonic spirals," Nano Letters 11, 2008­2016 (2011).
[24] Seng Fatt Liew, Heeso Noh, Jacob Trevino, Luca Dal Negro, and Hui Cao, "Localized photonic band edge modes and orbital angular momenta of light in a golden-angle spiral," Optics Express 19, 23631­23642 (2011).
[25] Jacob Trevino, Carlo Forestiere, Giuliana Di Martino, Selcuk Yerci, Francesco Priolo, and Luca Dal Negro, "Plasmonic-photonic arrays with aperiodic spiral order for ultra-thin film solar cells," Optics Express 20, A418­A430 (2012).
[26] Mani Razi, Ren Wang, Yanyan He, Robert M Kirby, and Luca Dal Negro, "Optimization of large-scale vogel spiral arrays of plasmonic nanoparticles," Plasmonics 14, 253­261 (2019).
[27] F. Sgrignuoli, R. Wang, F. A. Pinheiro, and L. Dal Negro, "Localization of scattering resonances in aperiodic vogel spirals," Phys. Rev. B 99, 104202 (2019).
[28] John A Adam, A mathematical nature walk (Princeton University, 2011). [29] Mikael C. Rechtsman and Salvatore Torquato, "Effective dielectric tensor for electromagnetic
wave propagation in random media," Journal of Applied Physics 103, 084901 (2008). [30] Jaeuk Kim and Salvatore Torquato, "Multifunctional Composites for Elastic and Electromag-
netic Wave Propagation," arXiv:1908.06662 (2019), arXiv:1908.06662. [31] Lukas Novotny and Bert Hecht, Principles of nano-optics (Cambridge University, 2012). [32] Craig F Bohren and Donald R Huffman, Absorption and scattering of light by small particles
(John Wiley & Sons, 2008).
23

[33] Jean-Michel Geffrin, Pierre Sabouroux, and Christelle Eyraud, "Free space experimental scattering database continuation: experimental set-up and measurement precision," Inverse Problems 21, S117 (2005).
[34] Bert Hecht, Beate Sick, Urs P Wild, Volker Deckert, Renato Zenobi, Olivier JF Martin, and Dieter W Pohl, "Scanning near-field optical microscopy with aperture probes: Fundamentals and applications," The Journal of Chemical Physics 112, 7761­7774 (2000).
[35] Andrea Alu` and Nader Engheta, "Plasmonic and metamaterial cloaking: physical mechanisms and potentials," Journal of Optics A: Pure and Applied Optics 10, 093002 (2008).
[36] Romain Fleury, Francesco Monticone, and Andrea Alu`, "Invisibility and cloaking: Origins, present, and future perspectives," Physical Review Applied 4, 037001 (2015).
[37] Andrea Alu`, David Rainwater, and Aaron Kerkhoff, "Plasmonic cloaking of cylinders: finite length, oblique illumination and cross-polarization coupling," New Journal of Physics 12, 103028 (2010).
[38] Joaquin Vanschoren, "Meta-learning: A survey," arXiv preprint arXiv:1810.03548 (2018). [39] Xiaoli Chen, Jinqiao Duan, and George Em Karniadakis, "Learning and meta-learning of
stochastic advection-diffusion-reaction systems from sparse measurements," arXiv preprint arXiv:1910.09098 (2019). [40] Xin He, Kaiyong Zhao, and Xiaowen Chu, "Automl: A survey of the state-of-the-art," arXiv preprint arXiv:1908.00709 (2019).
24

