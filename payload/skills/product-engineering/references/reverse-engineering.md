# Reverse engineering and REA

Select this branch to investigate an application/binary/protocol, reconstruct behavior or analyze Electron/ASAR/.NET/native artifacts. A source or method's existence does not establish access, installation or authorization for an active target.

1. Use kb-find to read the shared security frame and relevant project note. Methodology: `{{MEMORY_ROOT}}/PROJECTS/Маршрутизатор безопасности и обратной разработки.md`. Historical 43 routes and old checks do not verify the current PC.
2. Establish the target, artifact, authorized environment and required level: source/behavior/bytecode/native. Start with available static inventory; active interaction stays in your own or an explicitly authorized test environment under the current frame.
3. Verify actually available tools/MCPs and their capabilities. [REA](https://github.com/morluto/rea) is a candidate for connected analysis of applications, JavaScript/Electron, .NET, websites and native binaries. Its README says static JS needs no native engine; native analysis uses Hopper/Ghidra/IDA. Check current documentation for actual support during use.
4. This UI/workflow package does not register REA MCP. Before use, check whether it is installed and connected; do not pretend an absent toolkit is available. System installation/registration of new access is a separate specific step, not automatic setup from a link.
5. Follow Evidence → Finding → Path under the project methodology. Bind conclusions to artifact, path, command and observation; separate static hypotheses from reproduced behavior. For authorized implementation in your own project, proceed to [product-implementation](../../product-implementation/SKILL.md).
