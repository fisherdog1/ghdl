#![allow(dead_code)]
pub const MSGID_NOTE: u8 = 0;
pub const MSGID_FIRST_WARNID: u8 = 1;
pub const MSGID_WARNING: u8 = 39;
pub const MSGID_ERROR: u8 = 40;
pub const MSGID_FATAL: u8 = 41;

#[repr(u8)]
pub enum Warnid {
    Library,
    DeprecatedOption,
    UnexpectedOption,
    MissingXref,
    DefaultBinding,
    Binding,
    Port,
    ReservedWord,
    Pragma,
    NestedComment,
    Parenthesis,
    VitalGeneric,
    DelayedChecks,
    Sensitivity,
    Body,
    Specs,
    Universal,
    PortBounds,
    RuntimeError,
    DeltaCycle,
    MissingWait,
    Shared,
    Hide,
    Unused,
    Nowrite,
    LogicLoop,
    Others,
    Pure,
    AnalyzeAssert,
    Attribute,
    Useless,
    MissingAssoc,
    OpenAssoc,
    Conformance,
    UnkeptAttribute,
    UnhandledAttribute,
    Static,
    Elaboration,
}

impl Warnid {
    const VALUES: [Self; 38] = [
        Self::Library,
        Self::DeprecatedOption,
        Self::UnexpectedOption,
        Self::MissingXref,
        Self::DefaultBinding,
        Self::Binding,
        Self::Port,
        Self::ReservedWord,
        Self::Pragma,
        Self::NestedComment,
        Self::Parenthesis,
        Self::VitalGeneric,
        Self::DelayedChecks,
        Self::Sensitivity,
        Self::Body,
        Self::Specs,
        Self::Universal,
        Self::PortBounds,
        Self::RuntimeError,
        Self::DeltaCycle,
        Self::MissingWait,
        Self::Shared,
        Self::Hide,
        Self::Unused,
        Self::Nowrite,
        Self::LogicLoop,
        Self::Others,
        Self::Pure,
        Self::AnalyzeAssert,
        Self::Attribute,
        Self::Useless,
        Self::MissingAssoc,
        Self::OpenAssoc,
        Self::Conformance,
        Self::UnkeptAttribute,
        Self::UnhandledAttribute,
        Self::Static,
        Self::Elaboration,
    ];

    const IMAGES: [&'static str; 38] = [
        "library",
        "deprecatedoption",
        "unexpectedoption",
        "missingxref",
        "defaultbinding",
        "binding",
        "port",
        "reservedword",
        "pragma",
        "nestedcomment",
        "parenthesis",
        "vitalgeneric",
        "delayedchecks",
        "sensitivity",
        "body",
        "specs",
        "universal",
        "portbounds",
        "runtimeerror",
        "deltacycle",
        "missingwait",
        "shared",
        "hide",
        "unused",
        "nowrite",
        "logicloop",
        "others",
        "pure",
        "analyzeassert",
        "attribute",
        "useless",
        "missingassoc",
        "openassoc",
        "conformance",
        "unkeptattribute",
        "unhandledattribute",
        "static",
        "elaboration",
    ];
}
pub const WARNID_USIZE: usize = 38;
