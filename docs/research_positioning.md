# Research Positioning

## Relation to the Research and Professional Field

This prototype is positioned at the intersection of smart city IoT analytics, edge-cloud coordination, and zero-ETL data processing. It is relevant to digital government because city agencies increasingly depend on sensor networks to monitor transportation, energy demand, air quality, and public infrastructure. It is also connected to public procurement and supply chain modernization because government technology decisions often require evaluating whether new data architectures can improve service responsiveness, reduce operational cost, and support resilient infrastructure management.

## Practical Relevance of the Problem

A city-scale IoT network can generate continuous readings from thousands of devices. A traditional cloud-only pipeline may be easy to manage, but it can introduce latency and unnecessary data movement when every raw message must be centrally ingested before analysis. Ultra-low latency processing is important for traffic incidents, structural monitoring alerts, emergency response coordination, and environmental risk detection.

The prototype studies a practical and bounded problem: how to compare cloud-only batch ETL with an edge-cloud approach that performs local prioritization and sends compact summaries to the cloud. This problem is narrow enough to implement reproducibly, yet meaningful for real-world public-sector analytics and infrastructure resilience.

## Demonstration of Technical Implementation Ability

The repository demonstrates the ability to convert a research idea into a working technical system. It includes synthetic data design, preprocessing, a baseline algorithm, an improved algorithm, quantitative evaluation, visualization, documentation, and tests. The code is modular and designed so that another researcher can inspect assumptions, change parameters, run the experiment, and compare results.

The improved method is not just a different model; it represents an architectural idea. It changes where computation happens, how much data is sent to the cloud, and how events are detected from a combination of raw high-priority readings and compact edge summaries. This makes the project relevant to applied research in smart city analytics, edge-cloud systems, and public-sector digital infrastructure.

## Real-World Impact

A validated version of this line of work could help public institutions assess lower-latency analytics strategies for smart infrastructure monitoring, urban mobility management, environmental sensing, and resilient public services. It can also support more informed procurement decisions by providing a transparent method for comparing centralized cloud-only architectures against edge-cloud designs before large-scale investment.
