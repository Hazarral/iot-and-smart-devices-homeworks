Given the scope of the final assignment, our team has elected to submit an advanced IoT edge-computing project in place of the standard digital agriculture exercise. This project replaces the basic sensor/relay loop with a Reinforcement Learning-driven Traffic Optimizer designed to minimize intersection wait times via dynamic phase duration.

Below is the architectural mapping of our project against the required IoT development rubric.

#### 1. Hardware, Sensors, and Actuators (Exemplary)

Because recording real traffic via overhead cameras is physically infeasible and legally problematic, this project utilizes **SUMO (Simulation of Urban MObility)** as our hardware abstraction layer.

- **Sensors (Telemetry):** SUMO simulates induction loops and lane-area detectors across a 2-way crossroad. To bridge the gap between simulation and the "noisiness" of real-world IoT sensors, we actively introduce fuzzy data by randomly occluding/dropping vehicle data and introducing randomized speeds before telemetry transmission.
    
- **Actuators (Control):** The traffic light phase controllers act as our hardware actuators, receiving dynamic phase durations (green time) to optimize intersection flow.
    
- **Edge Hardware:** A **Raspberry Pi 4** serves as the localized edge-inference node, processing incoming telemetry and computing optimal phase durations in real-time.
    

#### 2. Network Connectivity & Data Pipeline (Exemplary)

Instead of a basic HTTP Azure Function, we rely on a lightweight, high-throughput **MQTT** pipeline optimized for edge deployments.

- We utilize **QoS 1 (At least once)**. QoS 2 overhead is unnecessary for this pipeline, as occasional duplicate packets simply serve as beneficial noise for the Reinforcement Learning model to generalize against.
    
- **Pipeline Flow:** `SUMO (State Gen)` $\rightarrow$ `Noise Injection` $\rightarrow$ `MQTT Broker` $\rightarrow$ `Raspberry Pi 4 (Edge Inference)` $\rightarrow$ `MQTT Broker` $\rightarrow$ `SUMO (Actuator Update)`
    

#### 3. Edge Control Logic: Reinforcement Learning via SAC (Exemplary)

Instead of hard-coded thresholds, the actuator control logic is driven by a **Soft Actor-Critic (SAC)** model implemented via **Stable Baselines 3 (SB3)** and **SUMO-RL**. SAC was chosen for its capability to handle continuous action spaces and its entropy maximization, which prevents the model from collapsing into sub-optimal phase strategies. Training is offloaded to dedicated hardware (Windows/Linux PC), with the finalized lightweight model exported to the Raspberry Pi 4.

**The Markov Decision Process (MDP) Architecture:**

**A. State Space (Observation)**

The Pi 4 observes the following localized telemetry:

1. **Cumulative Waiting Time:** Natively queried via SUMO.
    
2. **Queue Length:** Vehicle count across 4 vectors (North, South, East, West approaches).
    
3. **Current Light Phase:** Binary state monitoring (accounting for the fixed 5-second amber window).
    
4. **Current Phase Time:** The currently executing green time limit.
    
5. **Elapsed Phase Time:** Triggering the SAC agent to wake and infer when the current phase is nearing expiration.
    

**B. Action Space (Continuous)**

The SAC agent controls a continuous action space, outputting a specific float value bounded between **15.0 and 60.0 seconds**. This bounds the actuator, ensuring a hard maximum wait time limit (60s green + 5s amber = 65s max red time) for any given lane.

**C. Reward Function**

The primary objective is the minimization of total system waiting time. To frame this as a maximization problem for the SAC agent, the reward function is defined as the **maximization of the negative cumulative waiting time**, driving the state as close to $0$ as mathematically possible.