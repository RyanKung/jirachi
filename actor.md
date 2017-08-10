<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Ryan's Cave - 2017-08-01-actor-as-sranular</title>
        <script type="text/javascript" src="../js/MathJax/MathJax.js?config=TeX-AMS-MML_HTMLorMML-full,Safe"></script>
        <link rel="stylesheet" href="../css/default.css" />
        <link rel="stylesheet" href="../css/github.css" />
    </head>
    <body>
        <div id="header">
            <div id="logo">
                <a href="../">Ryan's Cave</a>
            </div>
            <div id="navigation">
                <a href="../">Home</a>
                <a href="../about.html">About</a>
                <a href="../contact.html">Contact</a>
                <a href="../archive.html">Archive</a>
            </div>
        </div>

        <div id="content">
            <div class="info">
    Posted on August  1, 2017
    
</div>

<h1>
<center>
Actor as Sranular, A Isomorphism Micro-services Architecture
</center>
</h1>
<center>
<h4>
Ryan J.K
</h4>
</center>
<center>
<h4>
ryankung(at)ieee.org
</h4>
</center>
<h2 id="i-preface">I Preface</h2>
<p>Micro-Services was introducted by Peter Rodgers and Juval Löwy in 2005 [1,2,3]. The philosophy of it essentially equals to the Unix philosophy of “Do one thing and do it well”. [4][5][6]:</p>
<ul>
<li><p>The services are small - fine-grained to perform a single function.</p></li>
<li><p>The organization culture should embrace automation of testing and deployment. This eases the burden on management and operations and allows for different development teams to work on independently deployable units of code.[7]</p></li>
<li><p>The culture and design principles should embrace failure and faults, similar to anti-fragile systems.</p></li>
<li><p>Each service is elastic, resilient, composable, minimal, and complete.[6]</p></li>
</ul>
<p>And as Leslie Lamport’s defination of distributed which in given in 2000, the micro-services architecture should always be a distributed system. In the viewpoint, a network of interconnected computers is a distributed system, and a single computer can be also be viewed as a distributed system in which the central control unit, the menory unit, and the input-output channels are sparate process. <em>A system is distributed is the message transmision delay is not negligible compared to the time between events in a single process</em>.[9]</p>
<p>In the fact, Addressing to the granularity of services, the realworld usecase of microservices architecture is usually either a distributed system or based on a distributed system such as some raft or paxos implementation like etcd[9], consul[10] and zookeeper[11].</p>
<p>Thus the “Unix Philosophy” of “Do one thing and do it well” is actually talking about the Philosophy of about the Distributed System archiecture“, which is also descriping how”micro-services architecture&quot; works.</p>
<h2 id="ii-none-causal-modeling">II None-causal modeling</h2>
<h3 id="think-in-the-domain">2.1 Think in the Domain</h3>
<p>The most popular modeling method of micro-services nowadays is DDD (Domain-Driven Design), which trying to bind the model with the concrete implementation. The premise of the DDD is to make the modeling of the function or service be focus on the core domain and domain logic.[15][16]</p>
<p>When talking about Domain-Driven Design, we usually connected it with the DSL (Domain-Specific Languages). There are two ways in which the modeling can be understood: descriptive and preciptive. A descriptive model represent an existing system Thus a presciptive model is one that can be used to construct the target system.[17]. DSLs always used prescriptive model as the term model, and the DDD is actually a equivalently descriptive modeling method.</p>
<p>In model theory, a first-order theory is called model complete if every embedding of models is an elementary embedding. Equivalently, every first-order formula is equivalent to a universal formula[18]. We known that if a DSLs is Turing Completed, then, we can call it as GPL(General Purpose Language). The GPL is acturally a model companion of The Turing Machine.</p>
<p>And when we said that a language <span class="math inline">\(l\)</span> covers a subset of <span class="math inline">\(P\)</span>, we can simply call this subset the <span class="math inline">\(domain\)</span> covered with <span class="math inline">\(l\)</span>. The subset of <span class="math inline">\(P\)</span> in that domain <span class="math inline">\(P_D\)</span> is equal to the subset of <span class="math inline">\(P\)</span> we can express with a language <span class="math inline">\(l\)</span> <span class="math inline">\(P_l\)</span>. So, we cannot ask a question like: “Does the language adequately cover the domain?”, <strong>since it always does, by definition</strong>.[17] And the definition can be also interept as that “<strong>DSL is always Model Complete, by definition</strong>”[17]</p>
<h3 id="none-causal-modeling">2.2 None-Causal Modeling</h3>
<p>There is two kind of languages for modeling a complex system: <strong>Causal (or block-oriented) languages</strong> and <strong>none-causal (or object-oriented) language</strong>.[12] The drawback of Causal Languages is: Needing to explicty specify the causality, which hampers modularity and reuse[19]. None-causal language is tried to solve the issue of cause language via allowing the user to avoid committing the model it self to a specific causality.[20]</p>
<h3 id="csp-and-fhm">2.3 CSP and FHM</h3>
<p>CSP (Communication Sequential Processes) is a typical None-Causal Language, for modeling the <code>Processes</code> of <code>Distributed System</code>, created by C.A.R Hoare, and still keeping update in nowadays(2015)[14]. It defined a process as this:</p>
<p>Let <span class="math inline">\(x\)</span> be an event and let <span class="math inline">\(P\)</span> be a process, Then <span class="math inline">\((x \rightarrow P)\)</span> (proounced “<span class="math inline">\(x\)</span> then <span class="math inline">\(p\)</span>”)</p>
<p>In 1983, when Lamport talk about CPS, he said: “It’s a fine language, or more precisely, a fine set of communication constructs. Hoare deserved his <strong>Turing award</strong>…,We really know that CSP is the right way of doing things…”[14]. But He also thinks that “While theorieticians are busy studying CPS, people out there in the real world are building Ethernets. And CSP doesn’t seem to me to be a very good model of Ethernets… CSP isn’t a very good language for describing this kind of algorithm(The MUTEX Problem), although it’s good for other kinds of algoithms.”[14]</p>
<p>Now we knew that the problem of distributed system in 1983 is the consensus problem. Which is means how do processes learn that a shared value was used or selected. In fact that in 1978 the core solution had already introduced by Leslie Lamport: The algorithms based on the logic timestamp(<strong>Lamport Timestamp</strong>)[21], but the algorithm hasn’t be applied until 1990, the year of invention of Paxos [22]. (which algorithm is worthing a Turing Award).</p>
<p>There is some other researchs based on <strong>TimeStamp</strong>, In research of Yale, they has developed a framework called <em>functional rective programming</em>, or FRP[8]. which is highly suited fro causal hybird modeling[9]. And, because the full power of a functional language is avaliable, it exhibits a high degree of modularity, allowing reuse of components and design patterns.[23] And <em>functional hybird modeling</em>, or FHM is a combined of FRP and none-causal languages. Which can be seen as a generalization of FRP, since FRP’s functions on singals are a special case of FHM’s relations on signals. FHM, like FRP, also allows the description of structurally dynamic models.[24]</p>
<p>And the same two key ideas between CSP and FRP are to give first-class status to relations on signals/messages and to provide constructs for discrete switch ing between relations.</p>
<h2 id="iii-isomorphism-with-actor-model">III Isomorphism with Actor Model</h2>
<h3 id="isomorphism-graphic">3.1 Isomorphism Graphic</h3>
<p>Lets recall that how people talk about the micro-services when they are talking about micro-services: Small, Testable, Robustness, Composable and Elastic. The graphic of the micro-services system should be like a vertex-edge map, all vertexs are symmetic thus they send messages to each orther for implement a complete function(figure 3.1). The vertex <span class="math inline">\(S_i\)</span> denotes the services, and the length <span class="math inline">\(l\)</span> of edgo of <span class="math inline">\((S_i, S_j)\)</span> denotes the cost time between services <span class="math inline">\(S_i,S_j\)</span>. With CSP modeling, the processing between <span class="math inline">\(S_i,S_j)\)</span> can be also present as <span class="math inline">\((S_j \rightarrow S_j)\)</span>.</p>
<center>
<img src="https://ryankung.github.io/images/fig_3_1.png" />
</center>
<center>
figure 3.1[25]
</center>
<p>And some Services <span class="math inline">\(S_i\)</span> maybe multi-processes and should have it’s workers like this.</p>
<center>
<img src="https://ryankung.github.io/images/fig_3_2.png" />
</center>
<center>
figure 3.2[25]
</center>
<p>In Figure 3.2., Services <span class="math inline">\(S_2\)</span> have three workers <span class="math inline">\(w_i; i\in[1,3]\)</span>. We can see that all vertexs are Isomorphism.</p>
<h3 id="actor-model">3.2 Actor Model</h3>
<p>Actor Model is an implementation of CSP (or lamport-timestamp based distributed FRP), invented by Carl Hewitt [24], which is also one of embers of 1970s AI wave (The second wave of AI). In Actor model, the model of processes of CSP are defined and structed with <code>Actor</code>, the actors can make local decisions, create more actors and send/response messages. The most famous implementation of Actor Model language is Erlang. Some people think golang’s goroutine or Python3’s coroutine are also implementation of CSP or Actor model, but actually they not, because of the mutable statement and memory sharing.</p>
<p>In actor model, the <code>Actors</code> whose controlling the event loop is called <code>Arbiter</code>. Thus the <code>Actors</code> whose sharing the IO loop of <code>Arbiter</code> and controll other <code>Actors as Workers</code> is called <code>Monitor</code>. So a classic <code>Arbiter-Monitor</code>-<code>Actor</code> may like this:</p>
<center>
<img src="http://quantmind.github.io/pulsar/images/actors.svg" />
</center>
<center>
figure 3.3[25]
</center>
<p>Thus the figure 3.2 should be represent as:</p>
<center>
<img src="https://ryankung.github.io/images/fig_3_4.png" />
</center>
<center>
figure 3.4[25]
</center>
<p>The Arbiter Actor here is actually a implementation of the vertex-edge map we descripted in Ch. 3.1. In real-world of enginering, the Arbiter maybe implement by Operator System itself, the VM, or just based on the network.</p>
<h3 id="lamport-timestamp-based-frp">3.3 Lamport timestamp based FRP</h3>
<p>If we think that a distributed FRP is just the FRP system based on lamport timestamp but not the real-word timestamp, then we can found that there is alot of FRP features in the current Actor Model based Micro-services system, Such as Composable and Elastic.</p>
<p>We can remodel the CSP actor model <span class="math inline">\((S_i \rightarrow S_j)\)</span> with <span class="math inline">\(( \rightarrow_{(t_n)} S_i(t,m;\theta) \circ S_j(t,m;\theta))\)</span>. Where <span class="math inline">\(\rightarrow\)</span> denotes the function of event stream. and the <span class="math inline">\(S_i(t,m;\theta)\)</span> is means that a monitor actor is listen to the message stream <span class="math inline">\((t,m)\)</span>, and it’s elastic rate is based on param <span class="math inline">\(\theta\)</span>. And with builted in lamport timestamp, we won’t meet the problem of consensus, because we will actuall knowns that which vectex is outdated or not.</p>
<h2 id="reference">Reference</h2>
<p>[1] Rodgers, Peter. “Service-Oriented Development on NetKernel- Patterns, Processes &amp; Products to Reduce System Complexity Web Services Edge 2005 East: CS-3”. CloudComputingExpo 2005. SYS-CON TV. Retrieved 3 July 2017.</p>
<p>[2] Löwy, Juval (October 2007). “Every Class a WCF Service”. Channel9, ARCast.TV.</p>
<p>[3] Löwy, Juval (2007). Programming WCF Services 1st Edition. pp. 543–553.</p>
<p>[4] Lucas Krause. Microservices: Patterns and Applications. ASIN B00VJ3NP4A.</p>
<p>[5]Lucas Krause. “Philosophy of Microservices?”.</p>
<p>[6]Jim Bugwadia. “Microservices: Five Architectural Constraints”.</p>
<p>[7] Li, Richard. “Microservices Essentials for Executives: The Key to High Velocity Software Development”. Datawire. Datawire, Inc. Retrieved 21 October 2016.</p>
<p>[8] Leslie Lamport, Times ,Clocks, and the Ordering of Events in a Distributed System</p>
<p>[9] A distributed, reliable key-value store for the most critical data of a distributed system. https://coreos.com/etcd/</p>
<p>[10] Service Discovery and Configuration Made Easy https://www.consul.io/</p>
<p>[11] Apache ZooKeeper is an effort to develop and maintain an open-source server which enables highly reliable distributed coordination. https://zookeeper.apache.org/</p>
<p>[12] [Andrew Kennedy. Programming Languages and Dimensions. PhdD thesis, University of Cambridge, Computer Laboratory, April 1996. Published as Technical Port No. 391.](https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-391.pdf)</p>
<p>[13] C.A.R Hoare, Communicatiing Sequential Process, May 18, 2015.</p>
<p>[14] Leslie Lamport, 1983 Invited Address, Solved Problems, Unsolved Problems and Non-problems in Concurrency.</p>
<p>[15] Domain-driven design http://dddcommunity.org/</p>
<p>[16] Evans, Eric (2004). Domain-Driven Design: Tackling Complexity in the Heart of Software. Addison-Wesley. ISBN 978-032-112521-7. Retrieved August 12, 2012..</p>
<p>[17] DSL Engineering, Designing, Implementing and Using Domain-Specific Languages, Markus Voelter, dslbook.org</p>
<p>[18] Chang, Chen Chung; Keisler, H. Jerome (1990) [1973], Model Theory, Studies in Logic and the Foundations of Mathematics (3rd ed.), Elsevier, ISBN 978-0-444-88054-3</p>
<p>[19] Frannois E. Cellier. Object-oriented modelling: Means of dealing with system complexity. In Proceeedings of the 15th Benelur Meeting on Systems and Control, Mierlo, The Netherland, pages 53-64, 1006 cited in Functional Hybird Modeling, Henrik Nilsson, John Peterson, and Paul Hudak, Department of Computer Science, Yale University, PADL 2003</p>
<p>[20] Henrik Nisson, John Perterson, and Paul Hudak, Department of Computer Science, Yale University. Functional Hybird Modeling</p>
<p>[21] Leslie Lamport, Time, Clocks and The Ordering of Events in a Distributed System. Jul 1978</p>
<p>[22] Leslie Lamport, The Simple Paxos, 2000</p>
<p>[23] Zhanyong Wan and Paul Hudak. Functional reactive programming from first princple. In proceeding s of PLDI’01: Symposium on Programming Language Design and Implementation, pages 202-202, June 2000.</p>
<p>[24] Henrik Nilsson, John Peterson, and Paul Hudak, Functional Hybird Modeling, Department of Computer Science, Yale University, PADL 2003</p>
<p>[24] Carl Hewitt; Peter Bishop; Richard Steiger (1973). “A Universal Modular Actor Formalism for Artificial Intelligence”. IJCAI.</p>
<p>[25] Design of Pulsar, A Actor Model based framework, http://quantmind.github.io/pulsar/design.html</p>

        </div>

        <div id="footer">
            Site proudly generated by
            <a href="http://jaspervdj.be/hakyll">Hakyll</a>
        </div>
    </body>
</html>
