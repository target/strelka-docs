## Frequently Asked Questions

### "Who is Strelka?"
[Strelka](https://en.wikipedia.org/wiki/Soviet_space_dogs#Belka_and_Strelka) is one of the second generation Soviet space dogs to achieve orbital spaceflight -- the name is an homage to [Lockheed Martin's Laika BOSS](https://github.com/lmco/laikaboss), one of the first public projects of this type and from which Strelka's core design is based.

### "Why would I want a file scanning system?"
File metadata is an additional pillar of data (alongside network, endpoint, authentication, and cloud) that is effective in enabling threat hunting, threat detection, and incident response and can help event analysts and incident responders bridge visibility gaps in their environment. This type of system is especially useful for identifying threat actors during [KC3 and KC7](https://en.wikipedia.org/wiki/Kill_chain#Computer_security_model). For examples of what Strelka can do, please read the [use cases](#use-cases).

### "Should I switch from my current file scanning system to Strelka?"
It depends -- we recommend reviewing the features of each and choosing the most appropriate tool for your needs. We believe the most significant motivating factors for switching to Strelka are:
* More scanners (40+ at release) and file types (60+ at release) than [related projects](#related-projects)
* Modern codebase (Go and Python 3.9+)
* Server components run in containers for ease and flexibility of deployment
* Performant, OS-native client applications compatible with Windows, Mac, and Linux
* OS-native client applications for Windows, Mac, and Linux
* Built using [libraries and formats](#architecture) that allow cross-platform, cross-language support

### "Are Strelka's scanners compatible with Laika BOSS, File Scanning Framework, or Assemblyline?"
Due to differences in design, Strelka's scanners are not directly compatible with Laika BOSS, File Scanning Framework, or Assemblyline. With some effort, most scanners can likely be ported to the other projects.

### "Is Strelka an intrusion detection system (IDS)?"
Strelka shouldn't be thought of as an IDS, but it can be used for threat detection through YARA rule matching and downstream metadata interpretation. Strelka's design follows the philosophy established by other popular metadata collection systems (Bro, Sysmon, Volatility, etc.): it extracts data and leaves the decision-making up to the user.

### "Does it work at scale?"
Everyone has their own definition of "at scale," but we have been using Strelka and systems like it to scan up to 250 million files each day for over a year and have never reached a point where the system could not scale to our needs -- as file volume and diversity increases, horizontally scaling the system should allow you to scan any number of files.

### "Doesn't this use a lot of bandwidth?"
Maybe! Strelka's client applications provide opportunities for users to use as much or as little bandwidth as they want.

### "Should I run my Strelka cluster on my Bro/Suricata network sensor?"
No! Strelka clusters run CPU-intensive processes that will negatively impact system-critical applications like Bro and Suricata. If you want to integrate a network sensor with Strelka, then use the [`filestream`] client application. This utility is capable of sending millions of files per day from a single network sensor to a Strelka cluster without impacting system-critical applications.

### "I have other questions!"
Please file an issue or contact the project team at [TTS-CFC-OpenSource@target.com](mailto:TTS-CFC-OpenSource@target.com).
