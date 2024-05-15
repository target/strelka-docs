# Strelka

Strelka is a real-time, container-based file scanning system used for threat hunting, threat detection, and incident response. Originally based on the design established by Lockheed Martin's [Laika BOSS](https://github.com/lmco/laikaboss) and similar projects, Strelka's purpose is to perform file extraction and metadata collection at enterprise scale.

Strelka differs from its sibling projects in a few significant ways:

- Core codebase is Go and Python 3.9+ 
- Server components run in containers for ease and flexibility of deployment 
- OS-native client applications for Windows, Mac, and Linux 
- Built using libraries and formats that allow cross-platform, cross-language support
