ASAN_GLOBAL_DS = "__asan_global_ds"
ASAN_VERSION_CHECK = "__asan_version_mismatch_check_v6"
ASAN_INIT_FN = "asan.module_ctor"
ASAN_DEINIT_FN = "asan.module_dtor"

ASAN_LIB_INIT = "__asan_init_v4"

ASAN_MEM_EXIT = ".LC_ASAN_EX"
ASAN_MEM_ENTER = ".LC_ASAN_ENTER"

MODULE_INIT = [
    "    .align    16, 0x90",
    "# BB#0:",
    "    pushq    %rax",
    ".Ltmp11:",
    "    callq    {}@PLT".format(ASAN_LIB_INIT),
    #"    callq    %s@PLT" % (ASAN_VERSION_CHECK),
    #"    leaq    {0}(%rip), %rdi".format(ASAN_GLOBAL_DS),
    #"    movl    ${global_count}, %eax",
    #"    movl    %eax, %esi",
    #"    callq    __asan_register_globals@PLT",
    "    popq    %rax",
    "    retq",
]

MODULE_DEINIT = [
    "    .align    16, 0x90",
    "# BB#0:",
    "    pushq    %rax",
    ".Ltmp12:",
    #"    leaq    {0}(%rip), %rdi".format(ASAN_GLOBAL_DS),
    #"    movl    ${global_count}, %eax",
    #"    movl    %eax, %esi",
    #"    callq    __asan_unregister_globals@PLT",
    "    popq    %rax",
    "    retq",
]

MEM_LOAD_COMMON = [
    "\tleaq {lexp}, {clob1}",
    "\tmovq {clob1}, {tgt}",
    "\tshrq $3, {tgt}",
    "\tmovb 2147450880({tgt}), {tgt_8}",
    "\ttestb {tgt_8}, {tgt_8}",
    "\tje {0}_{{addr}}".format(ASAN_MEM_EXIT),
]

MEM_LOAD_SZ = [
    "\tandl $7, {clob1_32}",
    "\taddl ${acsz_1}, {clob1_32}",
    "\tmovsbl {tgt_8}, {tgt_32}",
    "\tcmpl {tgt_32}, {clob1_32}",
    "\tjl {0}_{{addr}}".format(ASAN_MEM_EXIT),
    "\tcallq __asan_report_load{acsz}@PLT",
]

MEM_REG_SAVE = [
    # Save Regs
    "\tpushq {reg}",
]

MEM_REG_REG_SAVE_RESTORE = [
    "\tmov {src}, {dst}",
]

MEM_FLAG_SAVE = [
    "\tpushf",
]

MEM_FLAG_SAVE_OPT = [
    # Save Flags
    "\tlahf",
    "\tseto %al",
    #"\txchg %ah, %al",
    "\tpushq %rax",
]

MEM_FLAG_RESTORE = [
    "\tpopf",
]

MEM_FLAG_RESTORE_OPT = [
    # Restore Flags
    "\tpopq %rax",
    #"\txchg %ah, %al",
    "\tadd $0x7f, %al",
    "\tsahf",
]

MEM_EXIT_LABEL = [
    "{0}_{{addr}}:".format(ASAN_MEM_EXIT),
]

MEM_REG_RESTORE = [
    # Restore Regs
    "\tpopq {reg}",
]

STACK_POISON_BASE = [
    "\tleaq {pbase}, {reg}",
    "\tshrq $3, {reg}",
]

STACK_POISON_SLOT = "\tmovb $0xff, {off}({reg})"
STACK_UNPOISON_SLOT = "\tmovb $0x0, {off}({reg})"
STACK_ENTER_LBL = ".ASAN_STACK_ENTER_{addr}"
STACK_EXIT_LBL = ".ASAN_STACK_EXIT_{addr}"

CANARY_CHECK = "%fs:0x28"
LEAF_STACK_ADJUST = "leaq -256(%rsp), %rsp"
LEAF_STACK_UNADJUST = "\tleaq 256(%rsp), %rsp"
