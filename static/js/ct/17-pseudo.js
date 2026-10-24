/* A small, safe interpreter for OCR Exam Reference Language style pseudocode.
 *
 * It never runs JavaScript from the page: source is tokenised, parsed into a
 * tree and walked one statement at a time, with a step limit so a loop that
 * never ends stops with a friendly message. Supported:
 *   x = 5            print(x)            name = input("Name? ")
 *   if x > 3 then ... elseif x == 3 then ... else ... endif
 *   for i = 1 to 10 step 2 ... next i
 *   while x < 10 ... endwhile           do ... until x == 0   (repeat ... until too)
 *   array scores[5]    scores[0] = 7    list = [3, 1, 2]
 *   + - * / ^  MOD  DIV  == != < <= > >=  AND OR NOT  true false
 *   str() int() float() real()  s.length s.upper s.lower s.substring(i, n) s.left(n) s.right(n)
 *   // comments
 * CT.pseudo.run(src, opts) returns { ok, output, error, vars, steps };
 * CT.pseudo.steps(src, opts) returns a stepper for tracing, one line at a time.
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  var KEYWORDS = ["if", "then", "elseif", "else", "endif", "for", "to", "step", "next", "while", "endwhile", "do", "until",
    "repeat", "print", "input", "and", "or", "not", "mod", "div", "true", "false", "array"];

  function fail(line, msg) { var e = new Error(msg); e.ctLine = line; e.ctFriendly = true; throw e; }

  // ------------------------------------------------------------- tokens
  function tokenise(text, line) {
    var out = [], i = 0;
    while (i < text.length) {
      var c = text[i];
      if (c === " " || c === "\t") { i++; continue; }
      if (c === "/" && text[i + 1] === "/") break;
      if (c === '"' || c === "'" || c === "“" || c === "”") {
        var close = c === "“" ? "”" : c, j = i + 1, s = "";
        while (j < text.length && text[j] !== close && !(c === "“" && text[j] === '"')) { s += text[j]; j++; }
        if (j >= text.length) fail(line, "A piece of text is missing its closing quote mark.");
        out.push({ t: "str", v: s }); i = j + 1; continue;
      }
      if (/[0-9]/.test(c) || (c === "." && /[0-9]/.test(text[i + 1] || ""))) {
        var m = /^[0-9]*\.?[0-9]+|^[0-9]+/.exec(text.slice(i))[0];
        out.push({ t: "num", v: Number(m) }); i += m.length; continue;
      }
      if (/[A-Za-z_]/.test(c)) {
        var w = /^[A-Za-z_][A-Za-z0-9_]*/.exec(text.slice(i))[0], lw = w.toLowerCase();
        out.push(KEYWORDS.indexOf(lw) >= 0 ? { t: "kw", v: lw } : { t: "id", v: w });
        i += w.length; continue;
      }
      var two = text.substr(i, 2);
      if (["==", "!=", "<=", ">=", "<>"].indexOf(two) >= 0) { out.push({ t: "op", v: two === "<>" ? "!=" : two }); i += 2; continue; }
      if ("=<>+-*/^(),[].:".indexOf(c) >= 0) { out.push({ t: "op", v: c }); i++; continue; }
      fail(line, "I don't recognise the character " + c + " here.");
    }
    return out;
  }

  // ------------------------------------------------------- expressions
  function Expr(toks, line) { this.toks = toks; this.i = 0; this.line = line; }
  Expr.prototype.peek = function (k) { return this.toks[this.i + (k || 0)]; };
  Expr.prototype.is = function (t, v) { var x = this.peek(); return !!x && x.t === t && (v === undefined || x.v === v); };
  Expr.prototype.take = function (t, v, msg) {
    if (!this.is(t, v)) fail(this.line, msg || ("I was expecting " + (v || t) + " here."));
    return this.toks[this.i++];
  };
  Expr.prototype.done = function () { return this.i >= this.toks.length; };
  Expr.prototype.expr = function () { return this.or(); };
  Expr.prototype.or = function () {
    var a = this.and();
    while (this.is("kw", "or")) { this.i++; a = { k: "bin", op: "or", a: a, b: this.and() }; }
    return a;
  };
  Expr.prototype.and = function () {
    var a = this.not();
    while (this.is("kw", "and")) { this.i++; a = { k: "bin", op: "and", a: a, b: this.not() }; }
    return a;
  };
  Expr.prototype.not = function () {
    if (this.is("kw", "not")) { this.i++; return { k: "not", a: this.not() }; }
    return this.cmp();
  };
  Expr.prototype.cmp = function () {
    var a = this.add();
    while (this.is("op") && ["==", "!=", "<", "<=", ">", ">="].indexOf(this.peek().v) >= 0) {
      var op = this.toks[this.i++].v;
      a = { k: "bin", op: op, a: a, b: this.add() };
    }
    if (this.is("op", "=")) fail(this.line, "To compare two values use ==. A single = gives a variable a value.");
    return a;
  };
  Expr.prototype.add = function () {
    var a = this.mul();
    while (this.is("op", "+") || this.is("op", "-")) { var op = this.toks[this.i++].v; a = { k: "bin", op: op, a: a, b: this.mul() }; }
    return a;
  };
  Expr.prototype.mul = function () {
    var a = this.pow();
    while (this.is("op", "*") || this.is("op", "/") || this.is("kw", "mod") || this.is("kw", "div")) {
      var op = this.toks[this.i++].v;
      a = { k: "bin", op: op, a: a, b: this.pow() };
    }
    return a;
  };
  Expr.prototype.pow = function () {
    var a = this.unary();
    if (this.is("op", "^")) { this.i++; return { k: "bin", op: "^", a: a, b: this.pow() }; }
    return a;
  };
  Expr.prototype.unary = function () {
    if (this.is("op", "-")) { this.i++; return { k: "neg", a: this.unary() }; }
    if (this.is("op", "+")) { this.i++; return this.unary(); }
    return this.post();
  };
  Expr.prototype.args = function () {
    var list = [];
    this.take("op", "(");
    if (!this.is("op", ")")) {
      list.push(this.expr());
      while (this.is("op", ",")) { this.i++; list.push(this.expr()); }
    }
    this.take("op", ")", "A closing bracket ) is missing.");
    return list;
  };
  Expr.prototype.post = function () {
    var a = this.prim();
    for (;;) {
      if (this.is("op", "[")) { this.i++; var ix = this.expr(); this.take("op", "]", "A closing bracket ] is missing."); a = { k: "index", a: a, i: ix }; continue; }
      if (this.is("op", ".")) {
        this.i++;
        var name = this.take("id", undefined, "I was expecting a name after the dot, like .length or .upper").v;
        var args = this.is("op", "(") ? this.args() : null;
        a = { k: "member", a: a, name: name.toLowerCase(), args: args };
        continue;
      }
      return a;
    }
  };
  Expr.prototype.prim = function () {
    var x = this.peek();
    if (!x) fail(this.line, "This line stops before the end of the calculation.");
    if (x.t === "num") { this.i++; return { k: "lit", v: x.v }; }
    if (x.t === "str") { this.i++; return { k: "lit", v: x.v }; }
    if (x.t === "kw" && (x.v === "true" || x.v === "false")) { this.i++; return { k: "lit", v: x.v === "true" }; }
    if (x.t === "kw" && x.v === "input") { this.i++; var ia = this.args(); return { k: "input", a: ia[0] || null }; }
    if (x.t === "op" && x.v === "(") { this.i++; var e = this.expr(); this.take("op", ")", "A closing bracket ) is missing."); return e; }
    if (x.t === "op" && x.v === "[") {
      this.i++;
      var items = [];
      if (!this.is("op", "]")) { items.push(this.expr()); while (this.is("op", ",")) { this.i++; items.push(this.expr()); } }
      this.take("op", "]", "A closing bracket ] is missing.");
      return { k: "list", items: items };
    }
    if (x.t === "id") {
      this.i++;
      if (this.is("op", "(")) return { k: "call", name: x.v.toLowerCase(), args: this.args(), raw: x.v };
      return { k: "var", name: x.v };
    }
    if (x.t === "kw") fail(this.line, "'" + x.v + "' cannot go here.");
    fail(this.line, "I did not expect " + x.v + " here.");
  };

  function parseExpr(toks, line) {
    var p = new Expr(toks, line), e = p.expr();
    if (!p.done()) fail(line, "There is something extra at the end of this line: " + p.peek().v);
    return e;
  }

  // -------------------------------------------------------- statements
  function lower(t) { return t && t.t === "kw" ? t.v : null; }
  function parse(src) {
    var lines = String(src).replace(/\r/g, "").split("\n").map(function (text, n) {
      var toks = tokenise(text, n + 1);
      // "end if" and "end while" are read as endif and endwhile
      if (toks.length > 1 && toks[0].t === "id" && toks[0].v.toLowerCase() === "end" && KEYWORDS.indexOf("end" + String(toks[1].v).toLowerCase()) >= 0) {
        toks.splice(0, 2, { t: "kw", v: "end" + String(toks[1].v).toLowerCase() });
      }
      return { n: n + 1, toks: toks };
    }).filter(function (l) { return l.toks.length; });
    var pos = 0;

    function block(enders) {
      var body = [];
      while (pos < lines.length) {
        var l = lines[pos], k = lower(l.toks[0]);
        if (k === "else" && l.toks[1] && lower(l.toks[1]) === "if") k = "elseif";
        if (enders.indexOf(k) >= 0) return body;
        body.push(statement());
      }
      return body;
    }
    function expectEnd(start, what, ender) {
      if (pos >= lines.length) fail(start, "This " + what + " has no " + ender + ".");
    }
    function statement() {
      var l = lines[pos], t = l.toks, k = lower(t[0]), n = l.n;
      if (k === "if") {
        var thenAt = -1;
        for (var a = t.length - 1; a > 0; a--) if (lower(t[a]) === "then") { thenAt = a; break; }
        if (thenAt < 0) fail(n, "An if line must end with then.");
        var branches = [{ cond: parseExpr(t.slice(1, thenAt), n), body: null, line: n }];
        pos++;
        branches[0].body = block(["elseif", "else", "endif"]);
        var elseBody = null;
        for (;;) {
          expectEnd(n, "if", "endif");
          var cur = lines[pos], ck = lower(cur.toks[0]), skip = 1;
          if (ck === "else" && cur.toks[1] && lower(cur.toks[1]) === "if") { ck = "elseif"; skip = 2; }
          if (ck === "elseif") {
            var tAt = -1;
            for (var b = cur.toks.length - 1; b > 0; b--) if (lower(cur.toks[b]) === "then") { tAt = b; break; }
            if (tAt < 0) fail(cur.n, "An elseif line must end with then.");
            var br = { cond: parseExpr(cur.toks.slice(skip, tAt), cur.n), body: null, line: cur.n };
            pos++;
            br.body = block(["elseif", "else", "endif"]);
            branches.push(br);
            continue;
          }
          if (ck === "else") {
            if (elseBody) fail(cur.n, "This if already has an else.");
            pos++;
            elseBody = block(["elseif", "else", "endif"]);
            continue;
          }
          if (ck === "endif") { pos++; break; }
        }
        return { type: "if", line: n, branches: branches, elseBody: elseBody };
      }
      if (k === "for") {
        // for i = a to b [step s]
        if (!t[1] || t[1].t !== "id") fail(n, "A for loop needs a counter, like: for i = 1 to 10");
        if (!t[2] || t[2].v !== "=") fail(n, "A for loop needs = after the counter, like: for i = 1 to 10");
        var toAt = -1, stepAt = -1;
        for (var c = 3; c < t.length; c++) { if (lower(t[c]) === "to" && toAt < 0) toAt = c; if (lower(t[c]) === "step") stepAt = c; }
        if (toAt < 0) fail(n, "A for loop needs to, like: for i = 1 to 10");
        var loop = { type: "for", line: n, v: t[1].v, from: parseExpr(t.slice(3, toAt), n),
          to: parseExpr(t.slice(toAt + 1, stepAt > 0 ? stepAt : t.length), n),
          step: stepAt > 0 ? parseExpr(t.slice(stepAt + 1), n) : null };
        pos++;
        loop.body = block(["next"]);
        expectEnd(n, "for loop", "next " + loop.v);
        var nx = lines[pos];
        if (nx.toks[1] && nx.toks[1].t === "id" && nx.toks[1].v !== loop.v) fail(nx.n, "next " + nx.toks[1].v + " does not match the for loop on line " + n + ", which counts with " + loop.v + ".");
        loop.end = nx.n;
        pos++;
        return loop;
      }
      if (k === "while") {
        var w = { type: "while", line: n, cond: parseExpr(t.slice(1).filter(function (x, i2, arr) { return !(i2 === arr.length - 1 && lower(x) === "do"); }), n) };
        pos++;
        w.body = block(["endwhile"]);
        expectEnd(n, "while loop", "endwhile");
        w.end = lines[pos].n;
        pos++;
        return w;
      }
      if (k === "do" || k === "repeat") {
        if (t.length > 1) fail(n, k + " goes on a line of its own.");
        var dl = { type: "do", line: n };
        pos++;
        dl.body = block(["until"]);
        expectEnd(n, k + " loop", "until");
        var u = lines[pos];
        dl.cond = parseExpr(u.toks.slice(1), u.n);
        dl.end = u.n;
        pos++;
        return dl;
      }
      if (k === "print") {
        if (!t[1] || t[1].v !== "(") fail(n, "print needs brackets, like: print(\"Hello\")");
        var pe = new Expr(t.slice(1), n), args = pe.args();
        if (!pe.done()) fail(n, "There is something extra after print(...) on this line.");
        pos++;
        return { type: "print", line: n, args: args };
      }
      if (k === "array") {
        if (!t[1] || t[1].t !== "id" || !t[2] || t[2].v !== "[") fail(n, "Declare an array like this: array scores[5]");
        var size = parseExpr(t.slice(3, t.length - 1), n);
        if (t[t.length - 1].v !== "]") fail(n, "A closing bracket ] is missing.");
        pos++;
        return { type: "array", line: n, name: t[1].v, size: size };
      }
      if (["endif", "next", "endwhile", "until", "else", "elseif", "then", "to", "step"].indexOf(k) >= 0) {
        fail(n, "There is a " + k + " here without the line that starts it.");
      }
      // assignment: name = expr, or name[i] = expr
      var eq = -1, depth = 0;
      for (var e2 = 0; e2 < t.length; e2++) {
        if (t[e2].v === "[" || t[e2].v === "(") depth++;
        if (t[e2].v === "]" || t[e2].v === ")") depth--;
        if (depth === 0 && t[e2].t === "op" && t[e2].v === "=") { eq = e2; break; }
      }
      if (eq > 0 && t[0].t === "id") {
        var target = parseExpr(t.slice(0, eq), n);
        if (target.k !== "var" && target.k !== "index") fail(n, "The left of = must be a variable name.");
        if (eq === t.length - 1) fail(n, "Give " + t[0].v + " a value after the = sign.");
        pos++;
        return { type: "assign", line: n, target: target, expr: parseExpr(t.slice(eq + 1), n) };
      }
      if (t[0].t === "id" && t[1] && t[1].v === "(") {
        pos++;
        return { type: "expr", line: n, expr: parseExpr(t, n) };
      }
      fail(n, "I don't understand this line. Lines start with a variable, print, if, for, while or do.");
    }

    var program = block([]);
    if (pos < lines.length) fail(lines[pos].n, "There is a " + lower(lines[pos].toks[0]) + " here without the line that starts it.");
    return program;
  }

  // -------------------------------------------------------------- values
  function show(v) {
    if (v === true) return "True";
    if (v === false) return "False";
    if (Array.isArray(v)) return "[" + v.map(function (x) { return typeof x === "string" ? '"' + x + '"' : show(x); }).join(", ") + "]";
    if (typeof v === "number") return Number.isInteger(v) ? String(v) : String(Math.round(v * 1e10) / 1e10);
    if (v === undefined || v === null) return "";
    return String(v);
  }
  function kind(v) { return typeof v === "string" ? "text" : typeof v === "number" ? "a number" : typeof v === "boolean" ? "True or False" : "a list"; }
  function num(v, line, what) {
    if (typeof v !== "number") fail(line, "You can't use " + kind(v) + " " + (what || "in a calculation") + ". Use int() or float() to turn text into a number.");
    return v;
  }

  function evaluate(e, env, line, io) {
    switch (e.k) {
      case "lit": return e.v;
      case "var":
        if (!Object.prototype.hasOwnProperty.call(env, e.name)) fail(line, "The variable " + e.name + " has not been given a value yet.");
        return env[e.name];
      case "list": return e.items.map(function (x) { return evaluate(x, env, line, io); });
      case "neg": return -num(evaluate(e.a, env, line, io), line);
      case "not": return !truthy(evaluate(e.a, env, line, io), line);
      case "input": {
        var prompt = e.a ? show(evaluate(e.a, env, line, io)) : "";
        if (prompt) io.out.push(prompt);
        if (!io.inputs.length) {
          if (io.ask) { var got = io.ask(prompt); if (got === null || got === undefined) fail(line, "The program stopped while waiting for input."); return String(got); }
          fail(line, "The program asked for input, but there is no more test data.");
        }
        var given = String(io.inputs.shift());
        io.echo.push(given);
        if (prompt) io.out[io.out.length - 1] = prompt + given;
        else io.out.push(given);
        return given;
      }
      case "index": {
        var arr = evaluate(e.a, env, line, io), ix = evaluate(e.i, env, line, io);
        if (typeof arr === "string") {
          num(ix, line, "as a position");
          if (ix < 0 || ix >= arr.length) fail(line, "Position " + ix + " is outside the text, which has " + arr.length + " characters.");
          return arr[ix];
        }
        if (!Array.isArray(arr)) fail(line, "Only an array or text can be used with [ ].");
        num(ix, line, "as a position");
        if (ix < 0 || ix >= arr.length || !Number.isInteger(ix)) fail(line, "The array has " + arr.length + " places (0 to " + (arr.length - 1) + "), so position " + ix + " does not exist.");
        if (arr[ix] === undefined) fail(line, "Position " + ix + " of the array has not been given a value yet.");
        return arr[ix];
      }
      case "member": {
        var obj = evaluate(e.a, env, line, io), nm = e.name;
        var args = (e.args || []).map(function (x) { return evaluate(x, env, line, io); });
        if (nm === "length") { if (typeof obj === "string" || Array.isArray(obj)) return obj.length; fail(line, ".length only works on text and arrays."); }
        if (typeof obj !== "string") fail(line, "." + nm + " only works on text.");
        if (nm === "upper") return obj.toUpperCase();
        if (nm === "lower") return obj.toLowerCase();
        if (nm === "substring") { num(args[0], line); num(args[1], line); return obj.substr(args[0], args[1]); }
        if (nm === "left") { num(args[0], line); return obj.slice(0, args[0]); }
        if (nm === "right") { num(args[0], line); return args[0] ? obj.slice(-args[0]) : ""; }
        fail(line, "Text does not have a ." + nm + ". Try .length, .upper, .lower, .substring, .left or .right.");
        return null;
      }
      case "call": {
        var a = e.args.map(function (x) { return evaluate(x, env, line, io); });
        var f = e.name;
        if (f === "str") return show(a[0]);
        if (f === "int") {
          if (typeof a[0] === "number") return Math.trunc(a[0]);
          var s = String(a[0]).trim();
          if (!/^[-+]?\d+$/.test(s)) fail(line, "int() could not turn \"" + a[0] + "\" into a whole number.");
          return parseInt(s, 10);
        }
        if (f === "float" || f === "real") {
          var fv = Number(String(a[0]).trim());
          if (String(a[0]).trim() === "" || isNaN(fv)) fail(line, f + "() could not turn \"" + a[0] + "\" into a number.");
          return fv;
        }
        if (f === "len") { if (typeof a[0] === "string" || Array.isArray(a[0])) return a[0].length; fail(line, "len() needs text or an array."); }
        if (f === "asc") return String(a[0]).charCodeAt(0);
        if (f === "chr") return String.fromCharCode(num(a[0], line));
        fail(line, "I don't know a function called " + e.raw + "().");
        return null;
      }
      case "bin": {
        if (e.op === "and") return truthy(evaluate(e.a, env, line, io), line) && truthy(evaluate(e.b, env, line, io), line);
        if (e.op === "or") return truthy(evaluate(e.a, env, line, io), line) || truthy(evaluate(e.b, env, line, io), line);
        var x = evaluate(e.a, env, line, io), y = evaluate(e.b, env, line, io);
        switch (e.op) {
          case "+":
            if (typeof x === "string" && typeof y === "string") return x + y;
            if (typeof x === "string" || typeof y === "string") fail(line, "You can't add text and a number. Use str() to turn the number into text.");
            return num(x, line) + num(y, line);
          case "-": return num(x, line) - num(y, line);
          case "*":
            if (typeof x === "string" && typeof y === "number") return x.repeat(Math.max(0, y));
            return num(x, line) * num(y, line);
          case "/": if (num(y, line) === 0) fail(line, "You can't divide by zero."); return num(x, line) / y;
          case "mod": if (num(y, line) === 0) fail(line, "You can't use MOD 0."); return ((num(x, line) % y) + y) % y;
          case "div": if (num(y, line) === 0) fail(line, "You can't divide by zero."); return Math.floor(num(x, line) / y);
          case "^": return Math.pow(num(x, line), num(y, line));
          case "==": return x === y;
          case "!=": return x !== y;
          default:
            if (typeof x !== typeof y) fail(line, "You can't compare " + kind(x) + " with " + kind(y) + " using " + e.op + "." +
              (typeof x === "string" || typeof y === "string" ? " If the text came from input(), use int() on it first." : ""));
            if (e.op === "<") return x < y;
            if (e.op === "<=") return x <= y;
            if (e.op === ">") return x > y;
            return x >= y;
        }
      }
    }
    fail(line, "Something went wrong working this out.");
  }
  function truthy(v, line) {
    if (typeof v === "boolean") return v;
    fail(line, "A condition must be True or False, but this is " + kind(v) + ". Did you mean == ?");
  }

  // ------------------------------------------------------------ running
  // The walk is a generator so a debugger or trace table can stop after each line.
  function* walk(body, env, io) {
    for (var s = 0; s < body.length; s++) {
      var st = body[s];
      yield { line: st.line, kind: st.type };
      switch (st.type) {
        case "assign": {
          var v = evaluate(st.expr, env, st.line, io);
          if (st.target.k === "var") env[st.target.name] = Array.isArray(v) ? v.slice() : v;
          else {
            var arr = evaluate(st.target.a, env, st.line, io), ix = evaluate(st.target.i, env, st.line, io);
            if (!Array.isArray(arr)) fail(st.line, "Only an array can be given a value at a position.");
            num(ix, st.line, "as a position");
            if (ix < 0 || ix >= arr.length || !Number.isInteger(ix)) fail(st.line, "The array has " + arr.length + " places (0 to " + (arr.length - 1) + "), so position " + ix + " does not exist.");
            arr[ix] = v;
          }
          break;
        }
        case "print":
          io.out.push(st.args.map(function (a) { return show(evaluate(a, env, st.line, io)); }).join(" "));
          break;
        case "array": {
          var size = num(evaluate(st.size, env, st.line, io), st.line, "as an array size");
          var made = [];
          for (var q = 0; q < size; q++) made.push(undefined);
          env[st.name] = made;
          break;
        }
        case "expr": evaluate(st.expr, env, st.line, io); break;
        case "if": {
          var ran = false;
          for (var b = 0; b < st.branches.length && !ran; b++) {
            if (b > 0) yield { line: st.branches[b].line, kind: "elseif" };
            if (truthy(evaluate(st.branches[b].cond, env, st.branches[b].line, io), st.branches[b].line)) { ran = true; yield* walk(st.branches[b].body, env, io); }
          }
          if (!ran && st.elseBody) yield* walk(st.elseBody, env, io);
          break;
        }
        case "for": {
          var from = num(evaluate(st.from, env, st.line, io), st.line), to = num(evaluate(st.to, env, st.line, io), st.line);
          var step = st.step ? num(evaluate(st.step, env, st.line, io), st.line) : 1;
          if (step === 0) fail(st.line, "A for loop's step can't be 0.");
          for (var i = from; step > 0 ? i <= to : i >= to; i += step) {
            env[st.v] = i;
            yield* walk(st.body, env, io);
            yield { line: st.end, kind: "next" };
          }
          break;
        }
        case "while":
          while (truthy(evaluate(st.cond, env, st.line, io), st.line)) {
            yield* walk(st.body, env, io);
            yield { line: st.line, kind: "while" };
          }
          break;
        case "do":
          do {
            yield* walk(st.body, env, io);
            yield { line: st.end, kind: "until" };
          } while (!truthy(evaluate(st.cond, env, st.end, io), st.end));
          break;
      }
    }
  }

  function snapshot(env) {
    var o = {};
    Object.keys(env).forEach(function (k) { o[k] = Array.isArray(env[k]) ? env[k].slice() : env[k]; });
    return o;
  }

  CT.pseudo = {
    show: show,
    parse: function (src) {
      try { return { ok: true, program: parse(src) }; }
      catch (e) { if (!e.ctFriendly) throw e; return { ok: false, error: { line: e.ctLine, msg: e.message } }; }
    },
    // A stepper: next() runs one line and reports it, until done.
    steps: function (src, opts) {
      opts = opts || {};
      var max = opts.maxSteps || 5000, env = {}, io = { out: [], inputs: (opts.inputs || []).slice(), echo: [], ask: opts.ask };
      var p = CT.pseudo.parse(src), it = null, count = 0, finished = false, error = p.ok ? null : p.error;
      if (p.ok) it = walk(p.program, env, io);
      return {
        env: env, io: io,
        next: function () {
          if (finished || error) return { done: true, error: error, output: io.out, vars: snapshot(env) };
          try {
            var r = it.next();
            if (r.done) { finished = true; return { done: true, output: io.out, vars: snapshot(env) }; }
            count++;
            if (count > max) { error = { line: r.value.line, msg: "The program ran for too long. Is there a loop that never ends?" }; return { done: true, error: error, output: io.out, vars: snapshot(env) }; }
            return { done: false, line: r.value.line, kind: r.value.kind, output: io.out, vars: snapshot(env) };
          } catch (e) {
            if (!e.ctFriendly) throw e;
            error = { line: e.ctLine, msg: e.message };
            return { done: true, error: error, output: io.out, vars: snapshot(env) };
          }
        }
      };
    },
    run: function (src, opts) {
      var s = CT.pseudo.steps(src, opts), r, n = 0;
      do { r = s.next(); n++; } while (!r.done);
      return { ok: !r.error, error: r.error || null, output: r.output.slice(), vars: r.vars, steps: n - 1 };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
