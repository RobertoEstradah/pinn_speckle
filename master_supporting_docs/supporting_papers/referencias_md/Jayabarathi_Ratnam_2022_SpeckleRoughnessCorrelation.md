# Comparison of Correlation between 3D Surface Roughness and Laser Speckle Pattern for Experimental Setup Using He-Ne as Laser Source and Laser Pointer as Laser Source (Jayabarathi & Ratnam, 2022)

> Fuente: `Jayabarathi_Ratnam_2022_SpeckleRoughnessCorrelation.pdf` (convertido con pdftotext desde `master_supporting_docs/supporting_papers/referencias/`)
>
> Publicado en *Sensors* 2022, 22, 6003. DOI: 10.3390/s22166003. Licencia CC BY 4.0 (acceso abierto).

---

sensors

Article

Comparison of Correlation between 3D Surface Roughness and
Laser Speckle Pattern for Experimental Setup Using He-Ne as
Laser Source and Laser Pointer as Laser Source

Suganandha Bharathi Jayabarathi 1,2,* and Mani Maran Ratnam 2

                                         1 Faculty of Engineering and Computer Technology, AIMST University, Semeling,
                                              Bedong 08100, Kedah, Malaysia

                                         2 School of Mechanical Engineering, Engineering Campus, Universiti Sains Malaysia,
                                              Nibong Tebal 14300, Penang, Malaysia; mmaran@usm.my

                                         * Correspondence: suga@aimst.edu.my

Citation: Jayabarathi, S.B.; Ratnam,     Abstract: Correlation between 3D surface roughness and characteristic features extracted from
M.M. Comparison of Correlation           laser speckle pattern was done using an inexpensive laser pointer and a digital single lens reﬂex
between 3D Surface Roughness and         (DSLR) camera in previous research work. There had been no comparison work done between the
Laser Speckle Pattern for                experimental setup which uses a laser pointer, which has a diode laser as the laser source, and the
Experimental Setup Using He-Ne as        experimental setup, which uses a He-Ne laser as the laser source. As such, in the current work,
Laser Source and Laser Pointer as        a comparison study between two experimental setups was carried out. One experimental setup
Laser Source. Sensors 2022, 22, 6003.    was using a He-Ne laser, spatial ﬁlter, and charged coupled device (CCD) camera, while another
https://doi.org/10.3390/s22166003        experimental setup was using a laser pointer and DSLR camera. The laser beam was illuminated
                                         at angles of 30◦, 45◦, and 60◦ from the horizontal. When a laser beam falls on the surface, the beam
Academic Editor: Han Haitjema            gets scattered, and the scattered beam undergoes interference and produces speckle patterns which
                                         are captured using a camera. Using a Matlab program, the gray level co-occurrence matrix (GLCM)
Received: 23 April 2022                  characteristic features, such as contrast (GLCM), correlation (GLCM), energy (GLCM), entropy
Accepted: 1 July 2022                    (GLCM), homogeneity (GLCM), and maximum probability, and non-GLCM characteristic features,
Published: 11 August 2022                such as mean, standard deviation (STD), uniformity, entropy, normalized R, and white-to-black
                                         ratio (W/B), were extracted and correlated with 3D surface roughness parameters. The coefﬁcient
Publisher’s Note: MDPI stays neutral     of determination (R2) was determined for each case. Compared to the setup using a laser pointer,
with regard to jurisdictional claims in  the setup using a He-Ne laser gave better results. In the setup using the He-Ne laser, there were
published maps and institutional afﬁl-   correlations with a coefﬁcient of determination R2 ≥ 0.7 at illumination angles of 30◦, 45◦, and 60◦,
iations.                                 whereas in the setup using a laser pointer, there were correlations with R2 ≥ 0.7 at illumination
                                         angles of 30◦ and 45◦. Mean characteristic features had more correlations with R2 ≥ 0.7 in the case of
Copyright: © 2022 by the authors.        the angle of illumination of 45◦ (7 out of 36 correlations) and 60◦ (11 out of 82 correlations), while
Licensee MDPI, Basel, Switzerland.       R-normalized characteristic features had more correlations with R2 ≥ 0.7 in the case of the angle
This article is an open access article   of illumination of 30◦ (9 out of 38 correlations) for the setup using the He-Ne laser. Correlation
distributed under the terms and          (GLCM) had more correlations with R2 ≥ 0.7 in the case of the setup using a laser pointer (2 out of
conditions of the Creative Commons       2 correlations for illumination angle of 30◦, and 4 out of 19 correlations for an illumination angle
Attribution (CC BY) license (https://    of 45◦). Roughness parameters Sa and Sq had more correlations with R2 ≥ 0.7 for an illumination
creativecommons.org/licenses/by/         angle of 30◦ (1 out of 2 correlations each), and Sp and Sz had more correlations with R2 ≥ 0.7 for
4.0/).                                   an illumination angle of 45◦ (4 out of 19 correlations each) in the case of the setup using a laser
                                         pointer. The novelty of this work is (1) being a correlation study between 3D surface roughness and
                                         speckle pattern using a He-Ne laser and spatial ﬁlter, and (2) being a comparison study between two
                                         experimental setups on the correlation between 3D surface roughness and speckle pattern.

                                         Keywords: surface roughness; speckle pattern; milled surface; non-contact; optical technique

Sensors 2022, 22, 6003. https://doi.org/10.3390/s22166003  https://www.mdpi.com/journal/sensors
Sensors 2022, 22, 6003                                                                                                                                              2 of 18

                        1. Introduction

                              Surface roughness refers to ﬁnely spaced irregularities formed during the machining
                        process [1]. Surface roughness inﬂuences mechanical part parameters such as ﬁt, wear
                        resistance, fatigue strength, contact stiffness, vibration, and noise. These variables have
                        an impact on a product’s service life and dependability [2]. As a result, surface roughness
                        measurement is critical in the production process. Surface roughness can be measured
                        with either a contact or non-contact method. The stylus probe is a widely used contact
                        method in the industry. This technology, however, has some drawbacks, including a long
                        measuring time and the stylus accuracy being dependent on its tip radius, which means it
                        may not be able to reliably detect surfaces with crevices smaller than the stylus tip [3].

                              On the surface of soft materials, the stylus tip could cause a scratch. White light
                        interferometers [4,5], the focus variation method [6], and confocal microscopy [7] are the
                        most common non-contact methods for assessing 3D roughness parameters currently
                        accessible. Machine vision has a high measurement efﬁciency, a big data acquisition
                        capacity, high measurement accuracy, and ﬂexibility [2].

                              Statistical properties [8–10], wavelet transform [11], Tsallis threshold [12], neural
                        network [3], gray level co-occurrence matrix (GLCM) [10,13], lacunarity [14], spectral
                        speckle correlation [15–18], and contrast [19,20] are some of the techniques used in vision
                        methods for correlating characteristics features with surface roughness. Proﬁle roughness
                        parameters and areal roughness parameters are two types of surface roughness parameters.
                        The proﬁle roughness parameters are also referred to as two-dimensional or 2D roughness
                        parameters, whereas the areal roughness parameters are referred to as three-dimensional
                        or 3D roughness parameters [8,21–23].

                              Current vision approaches extract characteristics to correlate with 2D roughness
                        parameters [9,13,20,24,25]. However, machined surfaces are 3D in nature and, hence, 3D
                        surface roughness parameters should be measured [8]. Jayabarathi and Ratnam [10] used
                        characteristic features extracted from laser speckle patterns for correlation with 3D surface
                        roughness. The researchers used a laser pointer instead of a He-Ne or diode laser which
                        are widely used in the research works involving speckle patterns. However, no literature is
                        available on how the results obtained with the setup used by Jayabarathi and Ratnam [10]
                        compared to the experimental setup used by other researchers. It is essential to compare the
                        two different setups, as replacing the He-Ne laser and spatial ﬁlter setup with a laser pointer
                        simpliﬁes the experimental setup, and is also inexpensive compared to the commercial
                        He-Ne laser. This is a continuation of the work of Jayabarathi and Ratnam [10], where a
                        comparison is carried out between an experimental setup using a laser pointer and digital
                        single lens reﬂex (DSLR) camera and an experimental setup using a He-Ne laser, spatial
                        ﬁlter, and charged coupled device (CCD) camera. In addition to that, there is no publication,
                        to the authors’ best knowledge, on any research work involving a correlation study between
                        3D surface roughness and characteristic features extracted from laser speckle pattern where
                        the experimental setup consists of a He-Ne laser, spatial ﬁlter, and CCD camera. Moreover,
                        no comparison studies were done between the experimental setup using the He-Ne laser
                        and the experimental setup used by Jayabarathi and Ratnam [10].

                        2. Materials and Methods
                        2.1. Sample Preparation

                              Two samples with ﬁve surfaces each were machined on a CNC 5-axis milling machine
                        (DMU 40 monoBLOCK by Deckel Maho, Bielefeld, Germany) with a four ﬂute high-
                        speed steel (HSS) end mills cutter with a diameter of 12 mm. One of the most essential
                        advantages of high-speed steel is its ability to cut through materials at high speeds. Because
                        of the alloy’s unique combination of hardness, wear resistance, and high-temperature
                        characteristics, one may make use of this beneﬁt. HSS tools are also less expensive than
                        carbide tools, making them an excellent choice for high-mix, low-volume applications.
                        Sample 1 and sample 2 are the names of the two reference samples. Figure 1 shows the two
                        machined samples. Each sample has 5 surfaces, and the surfaces are labeled 1 to 10.
Sensors 2022, 22, x FOR PEER REVIEW                                                                                                                                                                                                                          3 of 18

Sensors 2022, 22, 6003                      applications. Sample 1 and sample 2 are the names of the two reference samples. Figure 1
                                            shows the two machined samples. Each sample has 5 surfaces, and the surfaces ar3eofla1-8

                                            beled 1 to 10.

                                                  (a)                                                                                                                                              (b)

                                            FFiigure 1. ((aa)) SSaammppllee 11 aanndd ((bb)) SSaammppllee 2 with numbering [10].

                                                  Each surfacee wwaassmmaacchhinineeddatatdidffieffreernetnmt macahcinhinginpgapraamraemteertse,rasn, danudsinugsinthge tAhleicAonlia-
                                            cInonﬁanitIenfFinocitues FMoiccursosMcoipcreobsycoBpreukbeyr ABrliuckoenra,AAliucsotnriaa,, tAhuesftorlilao,wthinegf3oDlloswurinfagce3rDousguhrnfaecses
                                            rpoaurgamhneetsesrsp[a2r6a]moefteearsch[2s6u]rfoafceeawcheresumrfeaacseuwreedr.eTmhearsouurgehdn. eTshsevraoluuegshanreesstavbaulluaetsedarine
                                            tTaabbulela1te[d10i]n. Table 1 [10].

                                            •• AArriitthhmmeettiicc mmeeaann hheeiigghhtt ((SSaa));;
                                            •• RRoooott--mmeeaann--ssqquuaarree hheeiigghhtt ((SSqq));;
                                            •• MMaaxxiimmuumm ppeeaakk hheeiigghhtt ((SSpp));;
                                            •• MMaaxxiimmuumm vvaalllleeyy ddeepptthh ((SSvv));;
                                            •• MMaaxxiimmuumm hheeiigghhtt ((SSzz));;
                                            •• TTeenn ppooiinntt hheeiigghhtt ((SS1100zz));;
                                            •• SSkkeewwnneessss ((SSsskk));;
                                            •• KKuurrttoossiiss ((SSkkuu));;
                                            •• RRoooott--mmeeaann--ssqquuaarree ggrraaddiieenntt ((SSddqq));;
                                            •• DDeevveellooppeedd iinntteerrffaacciiaall aarreeaa rraattiioo ((SSddrr))..

                                            TTaabbllee 11.. TTaabbuullaattiioonn ooff mmaacchhiinniinngg ppaarraammeetteerrssaanndd33DDrroouugghhnneessssppaarraammeetteerrssooffeeaacchhssuurrffaaccee[[1100]]..

SuSurNfrfaoa.ccee  SS(prpSipSn(ep1mrpeidp0ned0m)led0ed)le(Fmeemd(Fm/emRem1dai2/nmtR0e)ainteDo)(mfeCpmDout(mfh)et1Cpmuth)(tµSma 0()µ.S9ma31)(µSmq1(µ.)S1mq17)    Sp(µSmp )  Sv   Sv      Sz(µSmz )   S10(zSµ1m0z)  Ssk Ssk  SkSu ku           SSddqq           (SS%ddr)r
  No.                                                                                                                                                         (µm)             (µm)   (µm)         (µm)                                                       (%)
                                                                                                                                                                           (µm)                                                              0.161
      1                                                                                                                                                            4.070                   7.959        6.187                                                1.305
                                                                                                                                                                               3.889                              −0.044 2.415              00.1.16717
                                                                                                                                                                                                                                            000.1..21749721  11..355035
12                 10010000 120280 1 1 0.9311.0461.1117.3224.0780.081 3.8879.774 7.95195.855 6.1897.217 −0.004.4281 2.431.3598                                                                                                              00.1.39118       121...576395603
                                                                                                                                                                                                                                            00.2.14825       14..756950
2 43               100110000000  280644000  1  1  1.04116..1326521.32112..6576758.081911.8.603997.771643.7.1935615.8215645..670755 9.2111407..482236 0.28001..214756                                                       3.3639..4084542                   21..672326
                                               1                                                                                                                                                                                             0.185
35                 10010000 440760 1 1 1.3215.2541.6715.8169.80109.9486.7985.678 16.61095.62610.81266.608 0.1406.360 3.464.1242                                                                                                                              1.749
                                                                                                                                                                                                                                            00.3.11986
46                 10025000 600120 1 1 1.1602.7481.5607.90211.635.968113.1366.960 24.71725.64114.452.3122 0.2705.335 6.025.4473                                                                                                             00.1.18952       41..583605
7                  2500          280           1  0.968 1.156 5.437 8.607 14.045 6.387 −0.177 6.528                                                                                                                                         00.1.18953
58                 10025000 760440 1 1 1.2504.9741.8116.22510.947.8169 8.6768.327 19.61236.49616.670.8440 0.3−600.124 6.144.3274                                                                                                                             11..788282
                                                                                                                                                                                                                                                             11..781419
69                 25025000 120600 1 1 0.7418.0580.9012.3265.6881.617 6.9690.490 12.61481.106 5.1282.325 0.3305.000 2.437.1352
710                25025000 280760          1 1 0.9618.1131.1516.4175.4397.640 8.6067.377 14.01465.016 6.38107.246−0.107.7257 6.532.7815

8                  2500          440        1 0.974 1.225 7.169 6.327 13.496 7.440 −0.124 4.374 0.196 1.830
                                 600 2.21. Expe1ri.0m5e8nta1l .S3e2t6up 18.617 9.490 18.106 8.325 0.000 3.152 0.192 1.888
9                  2500

10                 2500          760        1 Figu1r.e1123sho1.w41s7exp9e.r6i4m0ent6al.3s7e7tup 16. .E0x1p6eri1m0e.2n4t6al se0t.u2p571 con3s.7is1t5ed o0f.a19H3e-N1e.8l1a1ser

                                            used as the laser source; the laser beam was cleaned and expanded using a spatial ﬁlter

                                            2s.e2t.uEpx. pTehriemlaensetarlbSeeatmupt1hen fell onto the milled surface and was scattered, and this scattered
                                            fslwbﬁdaicletisaettraeeetremtrredceFTtussrwiiuheetogsotndiienuustrddhrebploeeadaea.frsas2TwTietmnhrhtVesheesThnuezpaoCtlonegalwioCadcnsIsmkeseDtmeerlrererwlabcefxpsgaeenepoaremanseuetmttF(rnere1iiicrcmrnl:tea1eenht;.ee2wwFewtnr/nhofthaa1eerasifsm2rlcele.pchal5sanlalse–trapcoet7ee(curtn5sTuepw)tubdIroaFleeht1naFndtei.hdm)cdou.EehraTisxmwnnmrihpneaaeaeiesgllxsrullCteaitaclemodtCslCneeeetDdssaCrhniunoesDitcrnepnaafmdlcaemataccusaalmkeeebcanrlthesaeeadueinroppnaraedfnaexss(1dtdpJwpitAzeecastaercoInhusnk2nCder.0lssfeeVmcaimdsa-pcMtatemeautcsedt5hs..tr0ieiTenoTn,rdhgfnJheA,ed.eaaaIvns,iHsimuJedpaewraapf-ttgaNihainceainegsesl)

                                            together could be rotated. Experiments were conducted for the combination of illumination
                                            angle of the laser beam of 30◦, 45◦, and 60◦, and camera aperture sizes (f -number) of 4,

                                            5.6, 8, 11, and 16. The CCD camera was ﬁxed relative to the machined surface. Figure 3

                                            shows the laser speckle pattern from experimental setup 1 for one of the machined surfaces.

                                            Laser speckle images for each of the 10 machined surfaces were captured. The laser speckle

                                            pattern image was 768 × 576 pixels and saved in TIFF format.
Sensors 2022, 22, 6003  4 of 18

                        Figure 2. Experimental setup 1.

                        Figure 3. Laser speckle pattern from experimental setup 1.
                        2.3. Experimental Setup 2

                              Because this is a continuation of the work reported by Jayabarathi and Ratnam [10],
                        experimental setup 2 was the same as that previously published. Experimental setup 2
                        is shown in Figure 4. As illustrated in Figure 4a,b, a laser beam from a commercial laser
                        pointer (LX1 by Legamaster, Ahrensburg, The Netherlands) with a 5 mm diameter red
                        laser dot, wavelength between 630 and 680 nm, and maximum output less than 1 mW,
                        was focused onto the sample at the necessary angle. The scattered beam underwent
Sensors 2022, 22, 6003  2.3. Experimental Setup 2

                              Because this is a continuation of the work reported by Jayabarathi and Ratnam [10],
                        experimental setup 2 was the same as that previously published. Experimental setup 2 is
                        shown in Figure 4. As illustrated in Figure 4a,b, a laser beam from a commercial laser
                        pointer (LX1 by Legamaster, Ahrensburg, The Netherlands) with a 5 mm diamete5rorf e1d8
                        laser dot, wavelength between 630 and 680 nm, and maximum output less than 1 mW,
                        was focused onto the sample at the necessary angle. The scattered beam underwent in-
                        terference, resulting in a laser speckle pattern. The laser speckle pattern image of size
                        i3n8t7e2rfe×r2e5n9c2e,priexseulsltiwngasinacaqulaisreerdsupseicnkgleapSaotnteyrnC.aTmheeralaDseSrLsRp-eAc2k3le0,pJaatptearnn(iimmaaggee roefssoilzue-
                        3fotaaslthoe8infuocanf7d3roant2se8lcnc7oa×atllo2ehnfolnads32e×leget85xcnt79nt2uhleg22oo5prtos9n×phee2f+aix2xo5u8lpt5e5eflpi9lilrx5egsm2n+e5nhwa8plmsstmlia,il)xnl.esaimpengTgsalashh.scwii,)qrltTelaieapuunhesdsaisgexriitpwplerrewlrdeueaxiedtratspusheistmeewsrdanpiraneniititrtmnn.geeh1dtseaF8aeani-iSnnpn5gtot5pu1.aFna8rmpiyerg-p5amCu5a5trua.remsmasTmt5mwhue.oresTaaosslwhtmDehecnaSooalssLoveucwnRtethoros-aevAfawsdoeu2crsa3wteueso0dtsif,stotmeJhwoactupboimttoltashaonammcrbnk((loiuaSamftnacaAoluakbrMgfarf(oeilSa)ccfrbASuoteroocsMsinuocew)lysntuoSiswlttoeuiheoinnrntnaeshy-

                        (a)  (b)

                        FFiigguurree44..(a(a))EExxppereirmimenentatlaslesteutpup2 a2nadn(db)(bcl)ocsleo-suep-uvpievwieowf thoef tshaemspalme ipllluemililnuamteidnabtyedlabseyrlbaesaemr b[e1a0m].
                        [10].

                        Figure 5. Laser speckle pattern [10].

                        FigureT5h.eLlaasseerrssppecekclkelepapttaetrtner[n10s].obtained from all the ten milled surfaces were captured at
                        varioTuhsecloamsebrisnpaeticoknlse opfatttheernf-snoubmtabienreadnfdrosmhuattllerthsepeteend mseitltliendg soufrtfhaceecsawmeerrea.cTaphteuirlelud-
                        amt ivnaartiioounsacnogmleboinf athtieonlasseorf pthoeinft-enruumsebderwaansd30s°h,u4t5t°e,rasnpdee6d0°s, ethtteinfg-noufmthbeercuasmederwa.eTreh8e,
                        i1ll6u,m22in, aantidon32a,nwglheiloef tthhee slahsuetrteprosipneteerdussuesdedwwase3r0e◦1,/4550◦,,1a/1n0d06, 01◦/2, 0th0,eafn-ndu1m/4b0e0rsu, sreedsuwlteinreg
                        8in, 1468, 2sp2,ecaknlde p32a,ttwerhniliemtahgeessh. uAtltleerxsppeereimdsenutsaeldwwoerkrea1n/d50a,n1a/ly1s0is0,w1e/r2e00ca, rarniedd1o/u4t0o0nse,
                        rteimsueltoinnglyi.n 48 speckle pattern images. All experimental work and analysis were carried
                        out one time only.

                        2.4. Characteristic Features Extraction

                              In the case of experimental setup 1, using MATLAB 2021a software, the speckle pattern
                        image was cropped to a size of 51 × 51 pixels (maximum possible size) and converted from
                        an RGB image to a grayscale image. Figure 6 shows the cropped grayscale image for the
                        speckle pattern obtained for surfaces 1 to 10 at an illumination angle of 45◦ and f -number
                        of 8 for experimental setup 1.
Sensors 2022, 22, 6003  6 of 18

                        Figure 6. (a–j) The grayscale images of the laser speckle pattern image for each surface at an
                        illumination angle of 45◦, and f -number of 8.

                              In the case of experimental setup 2, using MATLAB 2021a software, the speckle pattern
                        image was cropped to a size of 101 × 101 pixels (maximum possible size) and converted
                        from an RGB image to a grayscale image. Figure 7 shows the cropped grayscale image for
                        the speckle pattern obtained for surfaces 1 to 10 at an illumination angle of 45◦, f -number
                        of 16, and shutter speed of 1/100 s for experimental setup 2.

                              The grayscale image was not subjected to any ﬁltering process to avoid the loss of
                        data caused by ﬁltering. Characteristic features based on the histogram, such as mean
                        intensity, root-mean-square intensity, energy, entropy, and texture-based parameters, such
                        as normalized roughness, and gray level co-occurrence matrix (GLCM)-based parameters,
                        such as maximum probability, correlation, contrast, energy, homogeneity, and entropy, were
                        extracted from the grayscale images. To differentiate the energy and entropy descriptors
                        that are obtained from histogram-based and GLCM-based parameters, energy and entropy
                        descriptors based on GLCM shall be addressed as energy (GLCM) and entropy (GLCM).
                        From the binary image, the white-to-black pixels ratio was obtained as a characteristic
                        feature. Coefﬁcients of determination (R2) from the correlation study between the extracted
                        characteristic features and 3D surface roughness were evaluated.
Sensors 2022, 22, 6003                                                                        7 of 18

                        Figure 7. (a–j) Grayscale images of the laser speckle pattern image for each surface at an illumination
                        angle of 45◦, f -number of 16, and shutter speed of 1/100 s.

                              Equations (1)–(12) [10,27] that were used to extract the characteristic features from the
                        image are as follows:
                        • Histogram-based (statistical) features

                                ◦ Mean

                              Mean of the gray value of the image m obtained from original image f(x,y) of size
                        M × N, given by Equation (1).

                            1  M−1 N−1
                           MN  x = 0y = 0
                        =∑ ∑ m             f (x, y)                                           (1)

                        where f (x,y) is the gray value of the pixel at coordinate (x,y).
                                ◦ Standard deviation

                              The standard deviation σ of an image is given by Equation (2).

                           L−1
                        σ = ∑ rj − m 2p rj
                                                                                              (2)

                           j=0
Sensors 2022, 22, 6003                                                                         8 of 18

                        where

                        rj is the jth gray level;
                        L is the total possible gray level value;
                        p(rj) is the probability of occurrences of rj;
                        m is the mean of gray values of the image.

                               ◦ Energy

                        The energy descriptor, which is also known as uniformity, measures how pixel values

                        are distributed, along with the gray level range, and can be calculated for the grayscale

                        image using Equation (3).

                                                                     L−1                 2     (3)

                                                   energy = ∑ p rj
                                                                           j=0

                        where

                        rj is the jth gray level;
                        L is the total possible gray level value;
                        p(rj) is the probability of occurrences of rj.

                               ◦ Entropy

                        The entropy descriptor provides information about the complexity of the image, as

                        given by Equation (4).

                                                              L−1

                                                   entropy = − ∑ p rj log2 p rj                (4)

                                                              j=0

                        where

                        rj is the jth gray level;
                        L is the total possible gray level value;
                        p(rj) is the probability of occurrences of rj.

                        • Texture features
                                 ◦ The normalised descriptor of roughness

                        The normalised descriptor of roughness R is as given in Equation (5).

                                                   R  =  1              −     +  1             (5)

                                                                           1        σ2
                                                                                 (L−1)2

                        where
                        σ2 is variance;
                        L is the total possible gray level value.

                        • Gray level co-occurrence matrix (GLCM)

                              Histogram-based texture descriptors do not provide any information about the spatial
                        relationship among pixels. This information can be obtained using the gray level co-
                        occurrence matrix (GLCM). The matrix holds the information of the number of times pixels
                        with intensities ri and rj occur in image f (x,y) in the position speciﬁed by the displacement
                        vector (distance between two pixels d, and angle between the two pixels from horizontal,
                        θ). In this work, as in the MATLAB software, default values of the displacement vector and
                        orientation of d = 1 and θ = 0◦ were used. The matrix is normalized as given in Equation (6).

                                                   Ng (i, j)            =     g(i, j)          (6)
                                                                           ∑i ∑j g(i, j)

                        where
                        Ng(i,j) is the normalized gray level co-occurrence matrix;
Sensors 2022, 22, 6003                                                                                  9 of 18

                        g(i,j) is the element of the gray level co-occurrence matrix.
                              The following texture-based features are computed using a normalized GLCM, Ng(i,j).
                                ◦ Maximum probability (GLCM) is given by Equation (7).

                               Maximum probability (GLCM) = max Ng(i, j)                                (7)

                               ◦ Correlation (GLCM) is given by Equation (8).

                               Correlation (GLCM) = ∑i ∑j(i − µi) j − µj Ng(i, j)                       (8)
                                                                                 σi σj

                        where

                        µi is the mean of the row sums of Ng(i,j);
                        µj is the mean of column sums of Ng(i,j);

                        σi is the standard deviation of row sums of Ng(i,j);
                        σj is the standard deviation of column sums of Ng(i,j).

                               ◦ Contrast (GLCM) is given by Equation (9).

                               Contrast (GLCM) = ∑ ∑(i − j)2Ng(i, j)                                    (9)

                                                   ij

                               ◦ Energy (GLCM) is given by Equation (10).

                               Energy (GLCM) = ∑ ∑ Ng2(i, j)                                            (10)

                                                                                 ij

                               ◦ Homogeneity (GLCM) is given by Equation (11).

                               Homogeneity (GLCM)  =                             ∑   ∑    Ng(i, j)      (11)
                                                                                         1 + |i − j|
                                                                                  i   j

                               ◦ Entropy (GLCM) is given by Equation (12).

                               Entropy (GLCM) = − ∑ ∑ Ng(i, j)log2Ng(i, j)                              (12)

                               ij

                        • From the binary image, the following characteristic features were extracted:
                                ◦ Total white pixels to total black pixels ratio (W/B).

                        3. Results and Discussion

                              Table 2 is the tabulation of R2 ≥ 0.7 for an illumination angle of 30◦ for experiment
                        setup 1. There are 38 correlations with an R2 ≥ 0.7. GLCM characteristic features account

                        for 11 of the 38 correlations, while non-GLCM characteristic features account for 27 of the 38.

                        Figure 8 shows the bar chart of the number of times a characteristic feature correlates with
                        R2 ≥ 0.7. A characteristic feature, R normalised, had 9 out of 38 correlations with R2 ≥ 0.7.

                        Figure 9 shows the bar chart of the number of times 3D surface roughness correlates with
                        R2 ≥ 0.7. The 3D roughness parameter S10z had 15 out of 38 correlations. Figure 10 shows
                        the bar chart of the number of times correlations with R2 ≥ 0.7 occurs for each f -number
                        setting. The camera setting with f -number 8 had 19 correlations with R2 ≥ 0.7. Maximum
                        probability (GLCM) vs. Sdr had the highest R2 of 0.8742.
Sensors 2022, 22, 6003                                                          10 of 18

                         Table 2. Tabulation of the number of times a correlation between characteristic features and 3D
                         surface roughness occurs with R2 ≥ 0.7 for an illumination angle of 30◦ for experimental setup 1.

                                     3D Surface Roughness Parameters

Characteristic Features  Sa  Sq  Sp  Sv  Sz  S10z  Ssk                Sku  Sdq  Sdr

 Correlation (GLCM).         1   1           1
    Energy (GLCM)
   Contrast (GLCM)           1   3           2
    Entropy (GLCM)
                                 1                                         1    1
Homogeneity (GLCM)
Maximum probability              1           4                             1    1

          (GLCM)             1   1           2
           Mean
            STD              1   3           2

        Uniformity               1           4                             2    2
          Entropy

      R normalised
         Contrast
            W/B

                         Figure 8. Bar chart showing the number of times a characteristic feature was involved in a correlation
                         with R2 ≥ 0.7 for an illumination angle of 30◦ for experimental setup 1.
Sensors 2022, 22, 6003  11 of 18

                        Figure 9. Bar chart showing the number of times a 3D surface roughness parameter was involved in
                        correlation with R2 ≥ 0.7 for an illumination angle of 30◦ for experimental setup 1.

                        Figure 10. Bar chart showing the number of times there was correlation with R2 ≥ 0.7 for each
                        f -number setting, for an illumination angle of 30◦ for experimental setup 1.

                              Table 3 is the tabulation of R2 ≥ 0.7 for an illumination angle of 45◦ for experiment
                        setup 1. It was found that there were 36 correlations with R2 ≥ 0.7. Of these, 11 out

                        of 36 correlations were GLCM characteristic features, and 25 out of 36 correlations were

                        non-GLCM characteristic features. Figure 11 shows the bar chart of the number of times a
                        characteristic feature correlates with R2 ≥ 0.7. The mean characteristic feature had 7 out
                        of 36 correlations with R2 ≥ 0.7. Figure 12 shows a bar chart of the number of times 3D
                        surface roughness correlates with R2 ≥ 0.7. The 3D roughness parameter S10z had 15 out
                        of 36 correlations. Figure 13 shows a bar chart of the number of times correlation with
                        R2 ≥ 0.7 occurs for each f -number setting. The camera setting with f -number 5.6 had
                        15 correlations with R2 ≥ 0.7. The highest R2 was for maximum probability (GLCM) vs.
                        Sdq, with R2 = 0.9297.
Sensors 2022, 22, 6003                                                          12 of 18

                         Table 3. Tabulation of the number of times a correlation between characteristic features and 3D
                         surface roughness occurs with R2 ≥ 0.7 for an illumination angle of 45◦ for experimental setup 1.

                                     3D Surface Roughness Parameters

Characteristic Features  Sa  Sq  Sp  Sv  Sz  S10z  Ssk                Sku  Sdq  Sdr

  Correlation (GLCM)             1                                         1    1
    Energy (GLCM)
   Contrast (GLCM)                           1
    Entropy (GLCM)
                                 1           2
Homogeneity (GLCM)
Maximum probability          1               1                             1    1

          (GLCM)             2   1           4
           Mean
            STD                  1                 2

        Uniformity               1           2
          Entropy
                                 1           2
      R normalised
         Contrast                1           2     2                       1
            W/B
                         1   1               1

                         Figure 11. Bar chart showing the number of times a characteristic feature involved in correlation with
                         R2 ≥ 0.7 for an illumination angle of 45◦ for experimental setup 1.
Sensors 2022, 22, 6003  13 of 18

                        Figure 12. Bar chart showing the number of times a 3D surface roughness parameter was involved in
                        correlation with R2 ≥ 0.7 for an illumination angle of 45◦ for experimental setup 1.

                        Figure 13. Bar chart showing the number of times correlation with R2 ≥ 0.7 occurred for each
                        f -number setting for an illumination angle of 45◦ for experimental setup 1.

                              Table 4 is the tabulation of the number of times a combination of correlation between
                        characteristic features and 3D surface roughness with R2 ≥ 0.7 occurred for an illumination
                        angle of 60◦ for experiment setup 1. It was found that there were a total of 82 correlations
                        with R2 ≥ 0.7. Of these, 39 out of 82 correlations were with GLCM characteristic features,
                        while 43 out of 82 correlations were with non-GLCM characteristic features. Figure 14
                        shows the bar chart of the number of times a characteristic feature correlates with R2 ≥ 0.7.
Sensors 2022, 22, 6003                                                          14 of 18

                         The mean characteristic feature had 11 out of 82 correlations with R2 ≥ 0.7. Figure 15 shows
                         the bar chart of the number of times 3D surface roughness had a correlation with R2 ≥ 0.7.
                         The 3D roughness parameter S10z had 24 out of 82 correlations with R2 ≥ 0.7. Figure 16
                         shows the bar chart of the number of times correlations with R2 ≥ 0.7 occurs for each
                         f -number setting. The camera setting with f -number 5.6 had 30 correlations with R2 ≥ 0.7.
                         The highest R2 value was for maximum probability (GLCM) vs. Sdr, with R2 = 0.9384.

                         Table 4. Tabulation of number of times a correlation between characteristic features and 3D surface
                         roughness occurs with R2 ≥ 0.7 for an illumination angle of 60◦ for experimental setup 1.

                                     3D Surface Roughness Parameters

Characteristic Features  Sa  Sq  Sp  Sv  Sz  S10z  Ssk                Sku  Sdq  Sdr

  Correlation (GLCM)                         1                             1    1
    Energy (GLCM)
   Contrast (GLCM)           1   2           2                             1    1
    Entropy (GLCM)
                             1   1           1                             1    1
Homogeneity (GLCM)
Maximum probability          1   3           3                             1    1

          (GLCM)             2   1           2                             1    1
           Mean
            STD              1   3       1   1                             1    1

        Uniformity           2   4           3                             1    1
          Entropy
                             1               1     2
      R normalised
         Contrast            1   2           3     1                       1    1
            W/B
                             1   3           3                                  1

                                             1                             1

                         1   1               1

                                             2                             2    2

                         Figure 14. Bar chart showing the number of times a characteristic feature was involved in correlation
                         with R2 ≥ 0.7 for an illumination angle of 60◦ for experimental setup 1.
Sensors 2022, 22, 6003  15 of 18

                        Figure 15. Bar chart showing the number of times a 3D surface roughness parameter was involved in
                        correlation with R2 ≥ 0.7 for an illumination angle of 60◦ for experimental setup 1.

                        Figure 16. Bar chart showing the number of times correlation with R2 ≥ 0.7 occurred for each
                        f -number setting for an illumination angle of 60◦ for experimental setup 1.

                              Table 5 is the tabulation of R2 ≥ 0.7 for an illumination angle of 30◦ for experiment
                        setup 2. It was found that there were two correlations with R2 ≥ 0.7 at the camera setting
                        with an f -number of 8 and shutter speed of 1/200 s. There was no correlation for non-GLCM
                        characteristic features. The only characteristic features with correlation were correlation
Sensors 2022, 22, 6003                                                                                              16 of 18

                        (GLCM) and roughness parameters Sa and Sq, each having a correlation of 1 out of 2. The
                        highest R2 was for correlation (GLCM) vs. Sq, with R2 = 0.7438.

                        Table 5. Tabulation of R2 ≥ 0.7 for an illumination angle of 30◦ for experimental setup 2.

                        S. No.           Correlation                   R2      Camera Setting
                           1    Correlation (GLCM) vs. Sa            0.7354
                           2    Correlation (GLCM) vs. Sq            0.7438  f -number 8, shutter
                                                                                speed 1/200 s

                              Table 6 is the tabulation of R2 ≥ 0.7 for an illumination angle of 45◦ for experimental
                        setup 2. It was found that there were 19 correlations with R2 ≥ 0.7. An f -number of 8 with a
                        shutter speed of 1/50 s had two correlations with R2 ≥ 0.7. An f -number of 16 with a shutter
                        speed 1/100 s had eight correlations with R2 ≥ 0.7. An f -number of 22 with a shutter speed
                        of 1/100 s had two correlations with R2 ≥ 0.7. An f -number of 22 with a shutter speed
                        1/200 s had seven correlations with R2 ≥ 0.7. In total, 13 out of 19 correlations were GLCM

                        characteristic features, and 6 out of 19 correlations were non-GLCM characteristic features.

                        The correlation (GLCM) characteristic feature had 4 out 19 correlations, and roughness
                        parameters Sp and Sz each had 4 out of 19 correlations. The highest R2 is for energy (GLCM)
                        vs. S10z, with R2 = 0.8955.

                        Table 6. Tabulation of R2 ≥ 0.7 for an illumination angle of 45◦ for experimental setup 2.

                        S. No.             Correlation         R2                Camera Setting
                           1       Entropy (GLCM) vs. Sa     0.8208   f -number 8, shutter speed 1/50 s
                           2       Entropy (GLCM) vs. Sq     0.7352
                           3                                 0.7347  f -number 16, shutter speed 1/100 s
                           4              Energy vs. Sp      0.7202
                           5        Energy (GLCM) vs. Sp     0.7015  f -number 22, shutter speed 1/100 s
                           6                                 0.7354  f -number 22, shutter speed 1/200 s
                           7              Energy vs. Sz      0.7565
                           8             Entropy vs. Sz      0.7704
                           9       Entropy (GLCM) vs. Sz     0.8916
                          10    Homogeneity (GLCM) vs. Sz    0.8955
                          11             Energy vs. S10z     0.8151
                          12       Energy (GLCM) vs. S10z    0.8294
                          13               W/B vs. Sdq       0.749
                          14                                 0.806
                          15               W/B vs. Sdr       0.7358
                          16       Contrast (GLCM) vs. Sa    0.8148
                          17     Correlation (GLCM) vs. Sa   0.7368
                          18       Contrast (GLCM) vs. Sq    0.8403
                          19     Correlation (GLCM) vs. Sq   0.7316
                                   Contrast (GLCM) vs. Sp
                                 Correlation (GLCM) vs. Sp
                                Correlation (GLCM) vs. S10z

                              Experimental setup 1 had correlations with R2 ≥ 0.7 at illumination angles of 30◦,
                        45◦and 60◦, whereas experimental setup 2 had correlations with R2 ≥ 0.7 only at illumina-
                        tion angles of 30◦ and 45◦. In the case of experimental setup 1, there were more non-GLCM

                        characteristic features compared with GLCM characteristic features. The mean character-
                        istic feature had more correlations with R2 ≥ 0.7 for illumination angles of 45◦ (7 out of
                        36 correlations) and 60◦ (11 out of 82 correlations), and R-normalized had more correlations
Sensors 2022, 22, 6003                                                                                                                                             17 of 18

                        with R2 ≥ 0.7 in the case of illumination angles of 30◦ (9 out of 38 correlations). Roughness
                        parameter S10z had more correlation with R2 ≥ 0.7 for all of the illumination angles (15 out
                        of 38 correlations for angle 30◦, 15 out of 36 correlations for angle 45◦, and 24 out of 82
                        correlations for angle 60◦) in the experimental setup 1. For experimental setup 2, correlation
                        (GLCM) characteristic features had more correlations with R2 ≥ 0.7 (2 out of 2 correlations
                        for an illumination angle of 30◦, and 4 out of 19 correlations for an illumination angle of 45◦).
                        Roughness parameters Sa and Sq had more correlations with R2 ≥ 0.7 for an illumination
                        angle of 30 (1 out of 2 correlations each), and Sp and Sz had more correlations with R2 ≥ 0.7
                        for an illumination angle of 45 (4 out of 19 correlations each) for experimental setup 2. The
                        reason for better correlation using experimental setup 1 compared to experimental setup 2
                        could be due to the expansion of the laser beam, which reduced the intensity of the laser
                        beam that fell onto the surface. In this way, pixel saturation can be avoided. Another reason
                        could be due to cleaning the laser beam of noise using a spatial ﬁlter.

                        4. Conclusions

                              From the results, it can be seen that there are good correlations between characteristic
                        features and 3D surface roughness in both the experimental setups. Experimental setup 1
                        gives a better correlation compared to experimental setup 2. In the case of experimental
                        setup 1, all the illumination angles had correlations with R2 ≥ 0.7, and in the case of
                        experimental setup 2, there were no correlations in the case of an illumination angle of
                        60◦. The illumination angle of 60◦ gave the highest number of correlations with R2 ≥ 0.7
                        in the case of experimental setup 1 (82 correlations), and the illumination angle of 45◦
                        gave the highest number of correlations with R2 ≥ 0.7 in the case of experimental setup 2
                        (19 correlations). Mean characteristic features had more correlation with R2 ≥ 0.7 in the
                        case of an angle of illumination of 45◦ and 60◦, and R normalized characteristic features
                        had more correlation with R2 ≥ 0.7 in the case of an angle of illumination of 30◦ for
                        experimental setup 1. Correlation (GLCM) had more correlation with R2 ≥ 0.7 in the
                        case of experimental setup 2. Roughness parameters Sa and Sq had more correlation with
                        R2 ≥ 0.7 for an illumination angle of 30◦, and Sp and Sz had more correlation with R2 ≥ 0.7
                        for an illumination angle of 45◦ in the case of experimental setup 2. A spatial ﬁlter that
                        cleans the laser beam and then expands the cleaned beam could be the reason for the better
                        result in the case of experimental setup 1. Previous works focus more on correlation studies
                        involving 2D roughness parameters, while current work is focused on the correlation
                        involving 3D surface roughness and characteristic features extracted from the laser speckle
                        pattern. The current work shows that although experimental setup 1 gives better results
                        compared to experimental setup 2, experimental setup 2 uses inexpensive components
                        and is simple compared to experimental setup 1, and there is room for improvement in
                        future work whereby the experimental setup 2 should be carried out by replacing the DSLR
                        camera with a webcam. The novelty of this work is that it is (1) a correlation study between
                        3D surface roughness and speckle pattern using a He-Ne laser and spatial ﬁlter; and (2) a
                        comparison study between two experimental setups on the correlation between 3D surface
                        roughness and speckle pattern.

                        Author Contributions: Conceptualization, S.B.J. and M.M.R.; methodology, S.B.J. and M.M.R.; soft-
                        ware, S.B.J.; formal analysis, S.B.J.; investigation, S.B.J.; writing—original draft preparation, S.B.J.;
                        writing—review and editing, S.B.J. and M.M.R.; supervision, M.M.R. All authors have read and
                        agreed to the published version of the manuscript.

                        Funding: This research received no external funding.

                        Institutional Review Board Statement: Not applicable.

                        Informed Consent Statement: Not applicable.

                        Data Availability Statement: Not applicable.
Sensors 2022, 22, 6003  18 of 18

                                            Acknowledgments: The authors would like to show their gratitude to University Science Malaysia
                                            (USM) and AIMST University for their exceptional support without which this paper and the research
                                            behind it would not have been possible.

                                            Conﬂicts of Interest: The authors declare no conﬂict of interest.

References

1. Degarmo, E.P.; Black, J.T.; Kohser, R.A. Materials and Processess in Manufacturing, 8th ed.; Prentice-Hall International: Upper
       Saddle River, NJ, USA, 1997; p. 288.

2. Liu, J.; Lu, E.; Yi, H.; Wang, M.; Ao, P. A new surface roughness measurement method based on a color distribution statistical
       matrix. Measurement 2017, 103, 165–178. [CrossRef]

3. Rifai, A.P.; Aoyama, H.; Tho, N.H.; Md Dawal, S.Z.; Masruroh, N.A. Evaluation of turned and milled surfaces roughness using
       convolutional neural network. Measurement 2020, 161, 107860. [CrossRef]

4. Agrawal, A.; Goel, S.; Rashid, W.B.; Price, M. Prediction of surface roughness during hard turning of AISI 4340 steel (69 HRC).
       Appl. Soft Comput. 2015, 30, 279–286. [CrossRef]

5. Manojlovic, L.M.; Zivanov, M.B.; Marincic, A.S. White-Light Interferometric Sensor for Rough Surface Height Distribution
       Measurement. IEEE Sens. J. 2010, 10, 1125–1132. [CrossRef]

6. Petzold, S.; Klett, J.; Schauer, A.; Osswald, T.A. Surface roughness of polyamide 12 parts manufactured using selective laser
       sintering. Polym. Test. 2019, 80, 106094. [CrossRef]

7. Tsigarida, A.; Tsampali, E.; Konstantinidis, A.A.; Stefanidou, M. On the use of confocal microscopy for calculating the surface
       microroughness and the respective hydrophobic properties of marble specimens. J. Build. Eng. 2021, 33, 101876. [CrossRef]

8. Goh, C.S.; Ratnam, M.M. Assessment of Areal (Three-Dimensional) Roughness Parameters of Milled Surface Using Charge-
       Coupled Device Flatbed Scanner and Image Processing. Exp. Tech. 2016, 40, 1099–1107. [CrossRef]

9. Xu, D.; Yang, Q.; Dong, F.; Krishnaswamy, S. Evaluation of surface roughness of a machined metal surface based on laser speckle
       pattern. J. Eng. 2018, 2018, 773–778. [CrossRef]

10. Jayabarathi, S.B.; Ratnam, M.M. Correlation Study of 3D Surface Roughness of Milled Surfaces with Laser Speckle Pattern. Sensors
       2022, 22, 2842. [CrossRef]

11. Mahashar, A.J.; Siddhi, J.H.; Murugan, M. Surface roughness evaluation of electrical discharge machined surfaces using wavelet
       transform of speckle line images. Measurement 2020, 149, 107029. [CrossRef]

12. Soares, H.C.; Meireles, J.B.; Castro, A.O.; Huguenin, J.A.O.; Schmidt, A.G.M.; da Silva, L. Tsallis threshold analysis of digital
       speckle patterns generated by rough surfaces. Phys. A Stat. Mech. Appl. 2015, 432, 1–8. [CrossRef]

13. Joshi, K.; Patil, B. Prediction of Surface Roughness by Machine Vision using Principal Components based Regression Analysis.
       Procedia Comput. Sci. 2020, 167, 382–391. [CrossRef]

14. Dias, M.R.B.; Dornelas, D.; Balthazar, W.F.; Huguenin, J.A.O.; da Silva, L. Lacunarity study of speckle patterns produced by rough
       surfaces. Phys. A Stat. Mech. Appl. 2017, 486, 328–336. [CrossRef]

15. Baradit, E.; Gatica, C.; Yáñez, M.; Figueroa, J.C.; Guzmán, R.; Catalán, C. Surface roughness estimation of wood boards using
       speckle interferometry. Opt. Lasers Eng. 2020, 128, 106009. [CrossRef]

16. Goch, G.; Peters, J.; Lehmann, P.; Liu, H. Requirements for the Application of Speckle Correlation Techniques to On-Line
       Inspection of Surface Roughness. CIRP Ann. 1999, 48, 467–470. [CrossRef]

17. Dhanasekar, B.; Mohan, N.K.; Bhaduri, B.; Ramamoorthy, B. Evaluation of surface roughness based on monochromatic speckle
       correlation using image processing. Precis. Eng. 2008, 32, 196–206. [CrossRef]

18. Toh, S.L.; Shang, H.M.; Tay, C.J. Surface-roughness study using laser speckle method. Opt. Lasers Eng. 1998, 29, 217–225.
       [CrossRef]

19. Tchvialeva, L.; Markhvida, I.; Zeng, H.; McLean, D.I.; Lui, H.; Lee, T.K. Surface roughness measurement by speckle contrast under
       the illumination of light with arbitrary spectral proﬁle. Opt. Lasers Eng. 2010, 48, 774–778. [CrossRef]

20. Leonard, L.C.; Toal, V. Roughness measurement of metallic surfaces based on the laser speckle contrast method. Opt. Lasers Eng.
       1998, 30, 433–440. [CrossRef]

21. Smith, G.T. Industrial Metrology: Surfaces and Roundness; Springer: London, UK, 2002.
22. Wang, T.; Xie, L.-j.; Wang, X.-b.; Shang, T.-y. 2D and 3D milled surface roughness of high volume fraction SiCp/Al composites.

       Def. Technol. 2015, 11, 104–109. [CrossRef]
23. Molnár, V. Minimization Method for 3D Surface Roughness Evaluation Area. Machines 2021, 9, 192. [CrossRef]
24. Zhang, X.; Zheng, Y.; Suresh, V.; Wang, S.; Li, Q.; Li, B.; Qin, H. Correlation approach for quality assurance of additive

       manufactured parts based on optical metrology. J. Manuf. Processes 2020, 53, 310–317. [CrossRef]
25. Fuji, H.; Asakura, T.; Shindo, Y. Measurement of surface roughness properties by means of laser speckle techniques. Opt. Commun.

       1976, 16, 68–72. [CrossRef]
26. ISO 25178-2:2012; Geometrical Product Speciﬁcations (GPS)—Surface Texture: Areal—Part 2: Terms, Deﬁnitions and Surface

       Texture Parameters. ISO: Geneva, Switzerland, 2012.
27. Marques, O. Practical Image and Video Processing using MATLAB; John Wiley & Sons: Hoboken, NJ, USA, 2011.
