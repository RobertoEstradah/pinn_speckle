# Feasibility study on solving the Helmholtz equation in 3D with PINNs (Schoder & Kraxberger, 2024)

> Fuente: `Schoder_Kraxberger_2024_Helmholtz3D_PINNs.pdf` (convertido con pdftotext desde `master_supporting_docs/supporting_papers/referencias/`)

---

arXiv:2403.06623v1 [physics.comp-ph] 11 Mar 2024

FEASIBILITY STUDY ON SOLVING THE HELMHOLTZ EQUATION IN 3D WITH PINNS
Stefan Schoder Institute of Fundamentals and Theory in Electical Engineering (IGTE)
Graz University of Technology 8010 Graz, Austria
stefan.schoder@tugraz.at
Florian Kraxberger Institute of Fundamentals and Theory in Electical Engineering (IGTE)
Graz University of Technology 8010 Graz, Austria
kraxberger@tugraz.at
ABSTRACT
Room acoustic simulations at low frequencies often face significant uncertainties of material parameters and boundary conditions due to absorbing material. We discuss the application of PhysicsInformed Neural Networks (PINNs) to solve the (forward) Helmholtz equation in three dimensions (3D), employing mini-batch stochastic gradient descent with periodic resampling every 100 iterations for memory-efficient training. Addressing the computational challenges posed by the extension of PINNs from 2D to 3D for acoustics, DeepXDE is used for implementing the forward PINN. The proposed numerical method is benchmarked against an analytical solution of a standing wave field in 3D. The PINN results are also compared to the Finite Element Method (FEM) solutions for a 3D wave field computed with openCFS. The alignment between PINN-generated solutions and analytical/FEM solutions shows the feasibility of PINNs modeling 3D acoustic applications for future inverse problems, and validating the accuracy and reliability of the proposed approach. Compared to FEM, establishing the PINN model took few hours (similar to the setup of a FEM simulation), the training took 38h to 42.8h (which is longer than the solution of the FEM simulation, which took 17min-19min), and the inference took 0.05 seconds being more than 20,000 times faster than the FEM benchmark openCFS using the same number of degrees of freedomwhen producing the results. Thereby, the insight is gained that 3D acoustic wave simulations in the frequency domain are feasible for forward PINNs and can predict complex wave behaviors in real-world applications.
Keywords PINNs · FEM · Helmholtz equation · DeepXDE · openCFS · Acoustics · Waves · 3D · PDE · Room Acoustics · Time-Harmonic Wave Field · Absorber
1 Introduction
Room acoustics simulations aim towards improving the acoustic performance of interior spaces by meeting specific criteria and predicting acoustic quality in advance of the construction phase. However, numerous challenges have to be overcome, including uncertain boundary conditions and the simulation of low-frequent wave phenomena [1, 2]. A comprehensive examination underscores the current obstacles, with a particular emphasis on the persisting challenge of errors arising from uncertain input parameters. A survey identified that about two-thirds of the acousticians judge uncertainties in input parameters as the foremost obstacle hindering more accurate simulation results [3]. In [4], simulations with the use of absorption coefficients from textbook tables showed inadequate prediction capabilities of reverberation time. These insights underscore the critical importance of using correct material data for the accurate

PINN for 3D Helmholtz equation

modeling of room acoustics simulations, manifesting the interest in using forward physics-informed neural networks (PINNs) and inverse PINNs in three-dimensional (3D) space [1]. The computation of the time-harmonic acoustic wave field in large 3D geometries represents a challenging frontier for numerical methods. Especially, the solutions to the Helmholtz equation in 3D are essential for understanding low-frequent room acoustic scenarios. Traditional numerical methods, such as Finite Element Methods (FEM), have provided valuable insights [5, 6], but their computational approach is limited, and the inverse estimation of parameters is challenging. In this context, PINNs show a promising supplement, leveraging the power of optimization and machine learning to tackle both the forward propagation of acoustics and the inverse estimation of material parameters of 3D acoustic fields.
This paper addresses the challenge associated by extending PINNs to solve the Helmholtz equation in 3D, presenting a methodological breakthrough facilitated by the integration of state-of-the-art mini-batch stochastic gradient descent optimization with periodic shuffling of the training data points. The PINN investigation is conducted within the DeepXDE framework [7] and compared to a continuously tested and validated [2, 8­17] FEM solver openCFS [18]. Physics-Informed Neural Networks offer a unique advantage, using the same optimization routines when establishing the forward PINN and the inverse PINN. By incorporating domain-specific knowledge and physical principles into the neural network architecture, PINNs have demonstrated a capacity to learn and predict complex solutions to partial differential equations [19, 20]. This study builds upon the success of PINNs in 1D and 2D acoustic simulations [1, 7, 21­24] (see Tab. 1, extending their application to the more challenging 3D acoustics problems. The goal is to model and predict wave phenomena in 3D space accurately.

Table 1: Literature overview on noteworthy public development projects solving acoustic fields.

Type Article, GIT Article, GIT
Article
Preprint Article
Preprint
Preprint

Name
DeepXDE: A Deep Learning Library for Solving Differential Equations Solving the frequency-domain acoustic VTI wave equation using physics-informed neural networks
Hyper-parameter tuning of physics-informed neural networks: Application to Helmholtz problems
FO-PINNs: A First-Order formulation for Physics Informed Neural Networks Helmholtz-equation solution in nonsmooth media by a physics-informed neural network incorporating quadratic terms and a perfectly matching layer condition
PINNs-TF2: Fast and User-Friendly Physics-Informed Neural Networks in TensorFlow V2
Physics-Informed Neural Networks for Acoustic Boundary Admittance Estimation

URL Ref.

GIT

[7]

GIT

[21]

[22]

[23] [24]

GIT

[25]

Preprint [26]

The article is structured as follows: Sec. 2 introduces the theoretical background of PINNs as self-supervised learning. Section 3 presents the numerical examples of 3D room-like geometry with different boundary conditions, differential equation forcing, and material parameters. This section also shows the training results and the comparison to the analytic solution and FEM solution by error analysis. Each numerical example is accompanied by a discussion of the results obtained. Finally, Sec. 4 summarizes the key findings and provides a roadmap for future research directions.

2 Physics-informed Neural Networks for the Helmholtz Equation in Acoustics

PINNs represent a cutting-edge fusion of neural networks and equation-based principles of physics, offering a bundle of possibilities for solving complex partial differential equations (PDEs) and simulating physical systems [19]. This innovative approach delegates implementation-associated challenges encountered in traditional computational methods, such as Finite Element Methods (FEM) or Finite Difference Methods, by seamlessly integrating computational domainspecific and mathematical equation-specific knowledge directly into the neural network architecture. Specifically, Figure 1 schematically shows how such a feed-forward (multi-layer perceptron [27, 28]) fully connected layer network is tailored to model the inhomogeneous Helmholtz equation

( + k2)p(, x) = f (, x)

(1)

where p  C3 is the time-harmonic acoustic pressure, k = /c is the wavenumber,  the angular frequency, c the speed of sound, f the forcing term, and  is the Laplacian operator.

To predict p^(, x) with a PINN, let N L(x) : Rdin  Rdout be a L-feed-forward neural network (FNN) (with (L - 1)hidden neural network layers), with N neurons in the -th layer (N0 = din , NL = dout ). The output at layer of a feed-forward neural network is calculated by repeated nonlinear activation-function  weighted tensor products of (i)

2

PINN for 3D Helmholtz equation
Neural Network

Partial Differential Equation Helmholtz Equation

No

Done

Yes

Loss Function

Figure 1: PINNs applied to Helmholtz equation.

inputs and (ii) bias vector and weight matrix (e.g. in the -th layer by W   RN×N-1 and b  RN , respectively), such that the FNN 1 is recursively defined by

input layer: N 0(x) = x  Rdin

hidden layers: N (x) =  W N -1(x) + b  RN , for 1    L - 1,

(2)

output layer: N L(x) = W LN L-1(x) + bL  Rdout ;

In the case of PINNs in 3D, x = (x, y, z) at the input layer, where (x, y, z) denotes the space directions of one point. The output prediction at the output layer L is calculated by

p^ =W LN L-1(x) + bL = W L W L-1N L-2(x) + bL-1 + bL = . . .

(3)

=N L  N L-1  · · ·  N 0  x = N (, x) ,

(4)

with g being a series of mapping functions. The network transformative operations can be summarized by a nonlinear operation N (, x) and a structure  collecting all weights and biases  = {W l, bl}1lL. During supervised learning, the neural network weights will be learned by labeled training data D = {xi, pi}iN=L1 of NL samples, and unlabeled training data T = {xi}Ni=U1 of NU samples, to approximate a continuous function mapping g(x) = p. T comprises two sets, the points in the domain Tf of NP DE samples and the points on the boundary Tb of NBC samples. The
neural network operator p^ = N (, x) can be interpreted as an approximation of g(x) = p, regarding optimality of the

discrepancy (error) described by the cost functional (loss function), e.g. based on mean squared error (MSE) for the

data loss

Ldata(, D)

=

1 NL

N i=1



pi

- p^i

2

(5)

with  ·  being the L2-norm. In general, the data loss can be combined with other types of loss (e.g., boundary loss or PDE loss) as described in sec. 3, resulting in a total loss Ltotal. According to the minimization problem

^ = arg min (dataLdata(, D) + pdeLpde(, T ),

(6)



the weights and biases  are adjusted to minimize the loss function L. The converged set of weights and biases  is the optimal prediction of these parameters, denoted by ^. Minimization can be achieved by gradient-based optimization

1Note that all the network parameters depend on the solution frequency . When the frequency of the problem is changing, the FNN must be retrained. This is similar to the FEM, where the solver must construct and invert the system matrices for different frequencies separately.

3

PINN for 3D Helmholtz equation

algorithms, like Adam [29] or LBFGS algorithm [30]. Using the gradient of the loss function L, the weights and biases are adapted iteratively to decrease L, typically using backpropagation [31] and automatic differentiation [32]. A
standard gradient descent algorithm updates the parameters such that

i+1 = i - ii L ,

(7)

with  representing the learning rate and i the epoch number.

The Helmholtz equation (1) is a second-order linear partial differential equation of hyperbolic type governing the
behavior of acoustic waves in the frequency domain. It is derived from the linear scalar wave equation in the time domain through separation of variables and an assumption of time-harmonic dependence p~(x, t) = p(x)e-it. In addition to (1), for the inhomogeneous Helmholtz equation on a restricted domain , forcing and boundary conditions (e.g.,
Dirichlet boundary condition at D and Neumann boundary N , where the two surfaces form the domain boundary denoted as  = D  N ) have to be considered, forming a well-posed system of equations

p(x) + k2p(x) = f (x), x   \  ,

(8a)

p(x) = 0, x  D ,

(8b)

p(x) · n = 0, x  N .

(8c)

Here, f (x) represents the known volume forcing term of the inhomogeneous Helmholtz equation and n is the outward pointing normal vector of N . The solution to the Helmholtz equation yields the acoustic pressure p(x), typically expressed as a complex number, at a specific location x. To incorporate the inherent physical knowledge into the neural network, the residual of the Helmholtz equation rPDE is integrated into the loss function. The residual of the PDE is

rPDE(x) = p^(x) + k2p^(x) - f (x) x  DPDE

LPDE(, Tf )

=

1 NPDE

NPDE i=1



rPDE(x)

2

(9)

and it is evaluated at randomly sampled collocation points x within the computational domain , forming the dataset

Tf

=

{xi

}NPDE
i=1

,

where

NPDE

is

the

number

of

sample

points

for

the

PDE

residual.

In

addition,

the

residuals

of

the

boundary conditions have to be integrated into the loss function too. The Dirichlet boundary condition residual rDBC

rDBC = p(x) x  DDBC ,

LDBC(, Tb1)

=

1 NDBC

NDBC i=1



rDBC(x)

2

(10)

is

sampled

at

the

respective

sampling

points

on

the

Dirichlet

boundary

D

forming

the

set

Tb1

=

{xi

}NDBC
i=1

,

where

NDBC is the number of sample points for the Dirichlet boundary D. Similarly, the Neumann boundary condition

residual rNBC is

rNBC = p(x) · n x  DNBC

LNBC(, Tb2)

=

1 NNBC

NNBC i=1



rNBC(x)

2 ,

(11)

which

is

sampled

at

the

respective

sampling

points

on

the

Neumann

boundary

N

forming

the

set

Tb2

=

{xi

}NNBC
i=1

,

where NNBC is the number of sample points for the Neumann boundary B. In the training process, incorporating the

BCs involves adding the residual of the BCs directly to the loss function as a mean squared error, corresponding to the

forward solution. This results in a total loss

Ltotal = dataLdata + PDELPDE + DBCLDBC + NBCLNBC ,

(12)

where data, PDE, DBC, and NBC are weighting factors for the individual loss terms. If not defined otherwise PDE = 1 for all used FNN.

3 Application
In this section, basic room application examples in 2D and 3D are presented to highlight the capabilities of PINNs when approximating solutions of the Helmholtz equation.

4

PINN for 3D Helmholtz equation

3.1 Example 1a - Analytic solution in 2D, Dirichlet

The example demonstrates2 the application of PINNs to solve the Helmholtz equation in a 2D domain with Dirichlet boundary conditions. The governing equation is eq. (1) with forcing of

f (x, y) = k2 sin(kx) sin(ky) ,

(13)

with the wave number of k = 2/, wavelength  = 1/2, and the solution is sought in a 2D spatial domain  = [0, 1]2.

This leads to the analytic solution

p(x, y) = sin(kx) sin(ky) .

(14)

The training process involves formulating a comprehensive loss function that incorporates the Helmholtz equation. For the Helmholtz equation, the loss term is defined in eq. (9). A homogeneous Dirichlet boundary condition p(x, y) = 0 with (x, y)   is enforced by a transform of the neural network solution N (x, y) to the acoustic pressure

p~(x, y) = x(x - 1)y(y - 1)N (x, y) .

(15)

The resulting total loss function for this example is equivalent to eq. (12) with data = NBC = DBC = 0, and therefore reduces to

L1a = LPDE .

(16)

The PINN is set up using DeepXDE (with the PyTorch backend), and the trained network is capable of predicting the acoustic pressure p~ within the specified 2D domain. Ten random collocation points per wavelength along each direction for training and 30 for testing are defined. A fully connected neural network of four layers depth (three hidden layers) and layer width of 150 neurons is used. A sinus activation function is used with Glorot uniform bias and weights initialization. The network is trained over 5000 iterations by the ADAM optimizer with a learning rate of 0.001, resulting in a test loss of 0.00571.3

To enforce the boundary conditions via the loss function using DBC = 100, 15000 iterations have been made, resulting in a test loss of 0.0761. Figure 2 shows the exact (analytical) solution, the PINN solution with constraint DBC, and the PINN solution with DBC modeled as an additional loss term. The figure shows the acoustic pressure of the whole domain.

1

1

1

1

0

0

0

0

-1

-1

-1

0

(a) Exact solution. 1

0 (b) PINN, constraint DBC.1

0 (c) PINN, DBC loss. 1

Figure 2: The real part of the acoustic pressure.

3.2 Example 1b - Analytic solution in 3D, Dirichlet

Consistently with the previous example in 3D the computational domain is denoted by  = [0, 1]3, the application of

PINNs to solve the Helmholtz equation is extended using Neumann boundary conditions. The governing equation is

eq. (1) with forcing

f (x, y, z) = 2k2 cos(kx) cos(ky) cos(kz) ,

(17)

2Details of this initial example can be found here https://deepxde.readthedocs.io/en/latest/demos/pinn_forward/
helmholtz.2d.dirichlet.html. 3The defined hyperparameters can be optimized using Ray Tune or scikit-optimize4.

5

PINN for 3D Helmholtz equation

with a wave number of k = 2/, wave length  = 1/2. This leads to an analytic solution of

p(x, y, z) = cos(kx) cos(ky) cos(kz) .

(18)

For the Helmholtz equation in 3D, the loss term is defined by eq. (9). A homogeneous Dirichlet boundary condition

p(x, y, z) = 0 with (x, y, z)   is enforced by a transform of the neural network solution N (x, y, z) to the acoustic

pressure

p~(x, y, z) = x(x - 1)y(y - 1)z(z - 1)N (x, y, z) .

(19)

The resulting total loss function for this example is equivalent to eq. (12) with data = NBC = DBC = 0, and therefore reduces to the one from the previous example (16). Similarly to the example shown in sec. 3.1, the PINN is set up using DeepXDE (PyTorch backend) with an updated input layer for the additional space domain.

The trained network is capable of predicting the acoustic pressure p~ within the specified 3D domain, with the same collocation points resolution as defined in the previous example. A fully connected neural network of four layers depth (three hidden layers) and layer width of 250 is defined. Instead of the gradient descent using all collocation points, a batch-gradient descent algorithm is used for RAM efficient optimization of the neural network weights with periodic random resampling of the training points after 100 iterations. A sinus activation function is used with Glorot uniform bias and weights initialization. The network is trained over 10000 iterations using the ADAM optimizer with a learning rate of 0.001, resulting in a test loss of 0.142.

In the case of enforcing the boundary conditions via the loss function using DBC = 100, 20000 iterations (layer-width 180 have been made, resulting in a test loss of 0.0152. Figure 3 shows the exact solution, the PINN solution with constraint DBC, and the PINN solution with DBC modeled as an additional loss term. The figure shows the acoustic pressure in a cut through the whole domain at z = 0.125. It is observed that the number of iterations required rises with the number of loss terms and rises with the spatial dimensions.

1

1

1

1

0

0

0

0

-1

0

(a) Exact solution. 1

-1 0 (b) PINN, constraint DBC.1

-1 0 (c) PINN, DBC loss. 1

Figure 3: The real part of the acoustic pressure at z = 0.125.

Until now, no feasible boundary conditions for room acoustic applications have been used. In room acoustic simulations, it is justified to use homogeneous Neumann boundary conditions as an approximation of the impedance jump between air and the room wall for low frequencies [2]. As a next step, the loss-term modeled homogeneous Dirichlet boundary condition (sound soft) will be replaced by a homogeneous Neumann boundary condition (sound hard wall).

3.3 Example 2a - Analytic solution in 3D, Room Acoustics

Following the previous example, the application of PINNs to solve the Helmholtz equation is extended to a 3D domain  = [0, 1]3 with enforced Dirichlet boundary conditions. The governing equation is eq. (1) with forcing of

f (x, y, z) = 2k2 sin(kx) sin(ky) sin(kz) ,

(20)

with a wave number of k = 2/ and wave length  = 1/2. This leads to an analytic solution of

p(x, y, z) = sin(kx) sin(ky) sin(kz) .

(21)

A homogeneous Neumann boundary condition p(x, y, z) · n = 0 with (x, y, z)   is considered by the loss function. The loss term is defined in eq. (12), with data = DBC = 0, NBC = 5, and PDE = 1. The PINN is set up

6

PINN for 3D Helmholtz equation

using DeepXDE (PyTorch backend) with a layer-width of 1805. The network is trained over 30000 iterations by the ADAM optimizer with a learning rate of 0.001, resulting in a test loss of 0.125.
Figure 4 shows the exact solution, the PINN solution with constraint DBC, and the PINN solution with DBC modeled as an additional loss term. The figure shows the acoustic pressure in a cut through the whole domain at z = 0.125. It is observed that the number of iterations required rises with the use of a Neumann boundary condition. Furthermore, iterating the final ADAM optimized network parameters with an L-BFGS optimizer for 15000 iterations brings down the test loss to 0.0142.

1

1

1

1

0

0

0

0

-1

-1

-1

0

(a) Exact solution. 1

0

(b) PINN ADAM. 1

0 (c) PINN ADAM & L-BFGS.

Figure 4: The real part of the acoustic pressure at z = 0 with NBC.

Another hyperparameter test was trying to predict both the real and the imaginary part of the acoustic pressure p, wherein the imaginary part is zero in the following example. As a consequence, when using the PINN for obtaining a complex acoustic pressure, it is suggested to train a network for the real and the imaginary part separately.

3.4 Example 2b - Comparison to FEM in 3D, Room Acoustics

As a follow-up to the previous 3D room acoustic example, the source is modeled more realistically by a point source in the center of the room modeled by

f (x, y, z)

=

2k2

cos(kx)

cos(ky)

cos(kz)e-

(x-0.5)2+(y-0.5)2 +(z-0.5)2 22

.

(22)

The results for this excitation, are studied for several parameters , being a measure for the sharpness of the source distribution. For   0, the source is very localized. In the current form, the source decreases it strength with   0. Until a parameter  > 0.1, the original resolution of the field quantities was well enough to resolve the source distribution, leading to a condition  < 6. As soon as this condition, does not hold, the resolution of the training data is too rough for the PINN to be accurate. For smaller  < 0.1, additional adaptive refinement was introduced, enriching the number of training points (recursively by five, for 10 iterations6) in areas where the residual rPDE were largest. After the enriching of training points, 3000 iterations were performed with the ADAM optimization following by 150000 iterations using the L-BFGS. With this strategy, 0.1 >  > 0.02 were predicted reasonable and a first step
to resolve spatial and amplitude multi-scales of the problem.

The FEM reference solution based on the same setup was carried out in openCFS [18]. Thereby, a sparse and a fine mesh are used as depicted in fig. 6. The sparse mesh discretizes the cube's edge by 20 linear elements (approximately 10 degrees of freedom per wave length) , resulting in a total number of 8000 elements, and the fine mesh discretizes the cube's edge by 80 linear elements (approximately 40 degrees of freedom per wave length), resulting in 512000 elements of the computational domain.

A relative error measure Errrel is evaluated, such that

Errrel =

Npts i=1

(pi,ref

-

pi)2

Npts i=1

(pi,ref )2

,

(23)

5The model coincides with the loss-term modeled Dirichlet boundary condition Helmholtz PINN from the previous example and
can be seen as an evolution of this model. 6https://deepxde.readthedocs.io/en/latest/demos/pinn_forward/burgers.rar.html

7

PINN for 3D Helmholtz equation

1

1

1

1

0

0

0

0

-1

-1

-1

0

(a)   

1

0

(b)  = 100

1

0

(c)  = 10

1

1

1

1

1

0

0

0

0

-1

-1

-1

0

(d)  = 1

1

0

(e)  = 0.1

1

0

(f)  = 0.05

1

1

1

1

1

0

0

0

0

-1

-1

-1

0

(g)  = 0.04

1

0

(h)  = 0.03

1

0

(i)  = 0.02

1

Figure 5: The real part of the acoustic pressure at z = 0.5.

8

PINN for 3D Helmholtz equation

(a) Sparse FEM mesh (FEM-sparse).

(b) Fine FEM mesh (FEM-fine).

Figure 6: Cross-section through the sparse and fine meshes used for the FEM computations at z = 0.5.

where Npts is the number of evaluation points, pi,ref is the reference pressure and pi is the pressure for which the agreement against the reference pressure should be quantified. The Npts = 10000 evaluation points have been placed to the locations where the PINN prediction is evaluated, i.e., a grid of 10 cm × 10 cm across the computational domain at
z = 0.5 m. To interpolate the FEM solution to this grid, the FE basis functions are evaluated at the according location in the respective element, as implemented in openCFS [18]. The errors are denoted as follows: ErrrPeINl N,FEMsparse is the error between the PINN solution and the FEM solution obtained with the sparse mesh, ErrrPeINl N,FEMfine is the error between the PINN solution and the FEM solution obtained with the fine mesh, and ErrrFeElM is the error between the FEM solutions obtained with fine and sparse meshes.

Table 2: Performance comparison between PINN and FEM. For FEM-sparse and FEM-fine the given durations are the CPU-hours, and for PINN the duration denotes the time on one GPU.


0.1 1.0 10.0 100.0

PINN-training
2374:40.4 2512:01.8 2280:20.0 2565:38.8

Duration (mm:ss)

PINN-prediction FEM-sparse

00:00.05 00:00.05 00:00.05 00:00.05

00:16.8 00:17.6 00:20.9 00:20.7

FEM-fine
17:44.8 17:18.8 19:00.0 19:19.5

ErrrPeINl N,FEMsparse
0.5754 0.0454 0.0300 0.0303

Error
ErrrPeINl N,FEMfine
0.9718 0.0997 0.0243 0.0249

E rrrFeElM
0.9275 0.0924 0.0352 0.0352

4 Conclusion
In this working paper, the potential of using PINNs to approximate forward solutions of the Helmholtz equation is demonstrated for geometrically simple 2D and 3D problems (square or cubic computational domains) with homogeneous Neumann and Dirichlet boundary conditions. Thereby, the readily available PINN framework deepXDE is used to implement the neural networks and their respective cost functions. Having very low training losses and excellent agreement with the analytical solutions, the results exhibit a promising ability of PINNs as forward solvers.
Regarding computational cost, Tab. 2 exhibits an interesting behavior: Using the trained PINN as a forward-pass solver for the PDE, it is orders of magnitude faster than using a FEM solver. This highlights the potential of trained PINNs as surrogate models within optimization frameworks. However, it has to be noted that a study regarding the generalization abilities of the PINN is required prior to using the PINN in an optimization framework.
Future work may include a hyperparameter optimization of the PINNs in order to achieve a smaller test loss. Additionally, it is subject to further research, how well the PINN approach generalizes to more complex geometries to be applicable in real-world problems, i.e. large complex non-cuboid shapes. Nevertheless, the results presented in this working paper encourage future work.
9

PINN for 3D Helmholtz equation
Data and code availability
The data and code is available on reasonable request from the authors.
References
[1] Johannes D Schmid, Philipp Bauerschmidt, Caglar Gurbuz, and Steffen Marburg. Physics-informed neural networks for acoustic boundary admittance estimation. 2023, doi:10.2139/ssrn.4545338. Preprint Available at SSRN 4545338.
[2] Florian Kraxberger, Eric Kurz, Werner Weselak, Gernot Kubin, Manfred Kaltenbacher, and Stefan Schoder. A validated finite element model for room acoustic treatments with edge absorbers. Acta Acustica, 7(48):1­19, October 2023, doi:10.1051/aacus/2023044.
[3] Cheol-Ho Jeong. Room acoustic simulation and virtual reality-technological trends, challenges, and opportunities. J. Swed. Acoust. Soc.(Ljudbladet), 1:27­30, 2022.
[4] Michael Vorländer. Computer simulations in room acoustics: Concepts and uncertainties. The Journal of the Acoustical Society of America, 133(3):1203­1213, 2013.
[5] Florian Kraxberger, Eric Kurz, Leon Merkel, Manfred Kaltenbacher, and Stefan Schoder. Finite element simulation of edge absorbers for room acoustic applications. In Fortschritte der Akustik -- DAGA 2023, pages 1292­1295, Hamburg, March 2023. Deutsche Gesellschaft für Akustik.
[6] Florian Kraxberger, Eniz Museljic, Eric Kurz, Florian Toth, Manfred Kaltenbacher, and Stefan Schoder. The nonlinear eigenfrequency problem of room acoustics with porous edge absorbers. In Arianna Astolfi, Francesco Asdrubali, and Louena Shtrepi, editors, Proceedings of the 10th Convention of the European Acoustics Association: Forum Acusticum 2023, pages 6159­6166, Torino, September 2023. European Acoustics Association.
[7] Lu Lu, Xuhui Meng, Zhiping Mao, and George Em Karniadakis. DeepXDE: A deep learning library for solving differential equations. SIAM Review, 63(1):208­228, 2021, doi:10.1137/19M1274067.
[8] Stefan Schoder, Michael Weitz, Paul Maurerlehner, Alexander Hauser, Sebastian Falk, Stefan Kniesburges, Michael Döllinger, and Manfred Kaltenbacher. Hybrid aeroacoustic approach for the efficient numerical simulation of human phonation. The Journal of the Acoustical Society of America, 147(2):1179­1194, 2020.
[9] Stefan Schoder, Clemens Junger, and Manfred Kaltenbacher. Computational aeroacoustics of the eaa benchmark case of an axial fan. Acta Acustica, 4(5):22, 2020.
[10] Stefan Schoder, Klaus Roppert, Michael Weitz, Clemens Junger, and Manfred Kaltenbacher. Aeroacoustic source term computation based on radial basis functions. International journal for numerical methods in engineering, 121(9):2051­2067, 2020.
[11] Stefan Schoder, Manfred Kaltenbacher, Étienne Spieser, Hugo Vincent, Christophe Bogey, and Christophe Bailly. Aeroacoustic wave equation based on pierce's operator applied to the sound generated by a mixing layer. In 28th AIAA/CEAS Aeroacoustics 2022 Conference, page 2896, 2022.
[12] Lorenzo Tieghi, Stefan Becker, Alessandro Corsini, Giovanni Delibra, Stefan Schoder, and Felix Czwielong. Machine-learning clustering methods applied to detection of noise sources in low-speed axial fan. Journal of Engineering for Gas Turbines and Power, 145(3):031020, 2023.
[13] Stefan Schoder, Florian Kraxberger, Sebastian Falk, Andreas Wurzinger, Klaus Roppert, Stefan Kniesburges, Michael Döllinger, and Manfred Kaltenbacher. Error detection and filtering of incompressible flow simulations for aeroacoustic predictions of human voice. The Journal of the Acoustical Society of America, 152(3):1425­1436, 2022.
[14] Paul Maurerlehner, Stefan Schoder, Johannes Tieber, Clemens Freidhager, Helfried Steiner, Günter Brenn, KarlHeinz Schäfer, Andreas Ennemoser, and Manfred Kaltenbacher. Aeroacoustic formulations for confined flows based on incompressible flow data. Acta Acustica, 6:45, 2022.
[15] Stefan Schoder, Étienne Spieser, Hugo Vincent, Christophe Bogey, and Christophe Bailly. Acoustic modeling using the aeroacoustic wave equation based on pierce's operator. AIAA Journal, pages 1­10, 2023.
[16] Stefan Schoder and Andreas Wurzinger. Dataset cylincf-01 creation pipeline: Circular cylinder in a cross flow, mach number 0.03 and reynolds number 200. arXiv preprint arXiv:2303.05265, 2023.
[17] Andreas Wurzinger, Florian Kraxberger, Paul Maurerlehner, Bernhard Mayr-Mittermüller, Peter Rucz, Harald Sima, Manfred Kaltenbacher, and Stefan Schoder. Experimental prediction method of free-field sound emissions using the boundary element method and laser scanning vibrometry. Acoustics, 6(1):65­82, 2024.
10

PINN for 3D Helmholtz equation
[18] S. Schoder and K. Roppert. openCFS: Open source finite element software for coupled field simulation ­ part acoustics, 2022.
[19] Maziar Raissi, Paris Perdikaris, and George E Karniadakis. Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations. Journal of Computational physics, 378:686­707, 2019.
[20] Stefan Schoder, Eniz Museljic, Florian Kraxberger, and Andreas Wurzinger. Post-processing subsonic flows using physics-informed neural networks. In Proceedings of 2023 AIAA Aviation Forum, pages 1­8, San Diego, June 2023. AIAA.
[21] Chao Song, Tariq Alkhalifah, and Umair Bin Waheed. Solving the frequency-domain acoustic VTI wave equation using physics-informed neural networks. Geophysical Journal International, 225(2):846­859, January 2021, doi:10.1093/gji/ggab010.
[22] Paul Escapil-Inchauspé and Gonzalo A. Ruz. Hyper-parameter tuning of physics-informed neural networks: Application to helmholtz problems. Neurocomputing, 561:126826, 2023, doi:10.1016/j.neucom.2023.126826.
[23] Rini J. Gladstone, Mohammad A. Nabian, and Hadi Meidani. Fo-pinns: A first-order formulation for physics informed neural networks. Arxiv Preprint, 2022, doi:10.48550/arxiv.2210.14320.
[24] Yanqi Wu, Hossein S. Aghamiry, Stephane Operto, and Jianwei Ma. Helmholtz-equation solution in nonsmooth media by a physics-informed neural network incorporating quadratic terms and a perfectly matching layer condition. Geophysics, 88(4):T185­T202, June 2023, doi:10.1190/geo2022-0479.1.
[25] Reza Akbarian Bafghi and Maziar Raissi. Pinns-tf2: Fast and user-friendly physics-informed neural networks in tensorflow v2. Arxiv Preprint, 2023, doi:10.48550/arXiv.2311.03626.
[26] Johannes Schmid, Philipp Bauerschmidt, Caglar Gurbuz, and Steffen Marburg. Physics-informed neural networks for acoustic boundary admittance estimation. Mechanical Systems and Signal Processing, 2023, doi:10.2139/ssrn.4545338. Preprint.
[27] Frank Rosenblatt. The perceptron: a probabilistic model for information storage and organization in the brain. Psychological review, 65(6):386, 1958.
[28] Simon Haykin. Neural networks: a comprehensive foundation. Prentice Hall PTR, 1998. [29] Diederik P Kingma and Jimmy Ba. Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980,
2014. [30] Dong C Liu and Jorge Nocedal. On the limited memory bfgs method for large scale optimization. Mathematical
programming, 45(1-3):503­528, 1989. [31] David E Rumelhart, Geoffrey E Hinton, and Ronald J Williams. Learning representations by back-propagating
errors. nature, 323(6088):533­536, 1986. [32] Atilim Gunes Baydin, Barak A Pearlmutter, Alexey Andreyevich Radul, and Jeffrey Mark Siskind. Automatic
differentiation in machine learning: a survey. Journal of Marchine Learning Research, 18:1­43, 2018.
11

