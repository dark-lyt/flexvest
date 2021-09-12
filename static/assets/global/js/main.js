function _(x) {
    return document.getElementById(x);
}
// And all over the site from now on you can get html elements by their id by simply using
//_("div1").innerHTML = "Hello World";
function restrict(elem) {
    var tf = _(elem);
    var rx = new RegExp;
    if (elem == "email") {
        rx = /[' "]/gi;
    } else if (elem == "e") {
        rx = /[' "]/gi;
    } else if (elem == "phone") {
        rx = /[^+0-9]/gi;
    } else if (elem == "uname") {
        rx = /[^a-z0-9]/gi;
    } else if (elem == "discount") {
        rx = /[^0-9]/gi;
    }
    tf.value = tf.value.replace(rx, "");
}

function emptyElement(x) {
    _(x).innerHTML = "";
}

function showElement(x) {
    var x = _(x);
    if (x.style.display == 'none') {
        x.style.display = 'block';
    } else {
        x.style.display = 'block';
    }
}

function hideElement(x) {
    var x = _(x);
    if (x.style.display == 'block') {
        x.style.display = 'none';
    } else {
        x.style.display = 'none';
    }
}

//function toggleElement(x,a,b,c,d,e){
function toggleElement(x) {
    var x = _(x);

    //find and hide others
    //hideElement(a); hideElement(b); hideElement(c); hideElement(d); hideElement(e); 
    //done*/

    if (x.style.display == 'block') {
        x.style.display = 'none';
    } else {
        x.style.display = 'block';
    }
}

function goTo(here) {
    window.location.href = here;
}

function reloadPage() {
    window.location.reload();
}
//------------------------------------------------------------------------------------------
function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
//-------------------------------------------------------------------------------------------
function copyText(c_txt) {
    var txt = _(c_txt);
    prompt("Select and copy the address in the box", txt.innerHTML);
}
//-------------------------------------------------------------------------------------------
function logcheck() {
    var un = _("un").value;
    var pw = _("pw").value;
    var k = document.querySelector('.keep').checked;

    if (un == "" || pw == "") {
        _("stat").innerHTML = "Fill out all of the form data";
        return false;
    } else {
        _("loginbtn").style.display = "none";
        _("stat").innerHTML = 'please wait... <img src="assets/img/fbk.gif" style="width:10%; height:10%"/>';
        var ajax = ajaxObj("POST", "login.php");
        ajax.onreadystatechange = function() {
            if (ajaxReturn(ajax) == true) {
                if (ajax.responseText == "login_failed") {
                    _("stat").innerHTML = "Login unsuccessful, please try again.";
                    _("loginbtn").style.display = "block";
                } else {
                    window.location = "./?u=" + ajax.responseText;
                }
            }
        }
        ajax.send("u=" + un + "&p=" + pw + "&k=" + k);
        return true;
    }
}
//-------------------------------------------------------------------------------------------
function send_reset() {
    var un = _("un").value;

    if (un == "") {
        _("stat1").innerHTML = "Please enter your Email or Username";
        return false;
    } else {
        _("sendbtn").style.display = "none";
        _("stat1").innerHTML = 'please wait... <img src="assets/img/fbk.gif" style="width:10%; height:10%"/>';
        var ajax = ajaxObj("POST", "forgot_pass.php");
        ajax.onreadystatechange = function() {
            if (ajaxReturn(ajax) == true) {
                if (ajax.responseText == "not_found") {
                    _("stat1").innerHTML = "Email/Username does not match any account on our system.";
                    _("sendbtn").style.display = "block";
                } else {
                    _("display").innerHTML = '<div class="alert alert-info">SUCCESS! An email with a password reset link has been sent to you. Please use the link to reset your password.</div>';
                    _("stat1").innerHTML = "";
                }
            }
        }
        ajax.send("u=" + un);
        return true;
    }
}
//-------------------------------------------------------------------------------------------
function reset_pass() {
    var pw = _("pw").value;
    var pw2 = _("pw2").value;
    var who = _("who").value;
    var o_p = _("o_p").value;

    if (pw == "" || pw2 == "") {
        _("stat2").innerHTML = "**Missing Parameters";
        return false;
    } else if (who == "" || o_p == "") {
        _("stat2").innerHTML = "**Invalid User Credentials";
        return false;
    } else if (pw != pw2) {
        _("stat2").innerHTML = "**Password Mismatch";
        return false;
    } else {
        _("resetbtn").style.display = "none";
        _("stat2").innerHTML = 'please wait... <img src="assets/img/fbk.gif" style="width:10%; height:10%"/>';
        var ajax = ajaxObj("POST", "forgot_pass.php");
        ajax.onreadystatechange = function() {
            if (ajaxReturn(ajax) == true) {
                if (ajax.responseText == "error") {
                    _("stat2").innerHTML = "An error occurred, Please try again";
                    _("resetbtn").style.display = "block";
                } else {
                    _("display").innerHTML = '<div class="alert alert-info">SUCCESS! Your Password has been reset successfully. Login with your new password now!</div>';
                    _("stat2").innerHTML = "";
                }
            }
        }
        ajax.send("pw=" + pw + "&pw2=" + pw2 + "&who=" + who + "&o_p=" + o_p);
        return true;
    }
}
//---------------------------------------------------------------------------------------------	
function upd_profile() {
    var fn = _("fullname").value;
    var pw = _("pw").value;
    if (un == "" || pw == "") {
        _("stat").innerHTML = "Fill out all of the form data";
        return false;
    } else {
        _("loginbtn").style.display = "none";
        _("stat").innerHTML = 'please wait <img src="img/fbksmall.gif"/>';
        var ajax = ajaxObj("POST", "login.php");
        ajax.onreadystatechange = function() {
            if (ajaxReturn(ajax) == true) {
                if (ajax.responseText == "login_failed") {
                    _("stat").innerHTML = "Login unsuccessful, please try again.";
                    _("loginbtn").style.display = "block";
                } else {
                    window.location = "index.php?u=" + ajax.responseText;
                }
            }
        }
        ajax.send("u=" + un + "&p=" + pw);
        return true;
    }
}
/*----------------------------------------------------------------------------------------------
function sendM(e){
	if(e == ""){
		_("e-body").innerHTML = "Missing Parameters";
		return false;
	} else {
		_("e-btn").style.display = "none";
		_("e-body").innerHTML = 'please wait <img src="img/fbksmall.gif"/>';
		var ajax = ajaxObj("POST", "includes/parse/sendMail.php");
        ajax.onreadystatechange = function() {
	        if(ajaxReturn(ajax) == true) {
	            if(ajax.responseText == "sent"){
				   	_("e-body").innerHTML = "<font color='green'><b>Email has been sent. Remember to check your spam folders. Then click on the link for activation.</b></font>";
				} else {
					//_("e-body").innerHTML = ajax.responseText;
					_("e-body").innerHTML = "<font color='red'><b>Email could not be sent at the moment, please try again.</b></font>";
					_("e-btn").style.display = "block";
				}
	        }
        }
	ajax.send("email="+e);
	return true;
	}
}
//-----------------------------------------------------------------------------------------------*/
function sendMail(r) {
    // r can take two values, "admin" or "user".
    var bod = _("m_body");
    var btn = _("m_btn");
    //alert(r+bod+btn);
    //return false;
    btn.style.display = "none";
    bod.innerHTML = 'please wait... <img src="assets/img/fbk.gif" style="width:10%; height:10%"/>';
    var ajax = ajaxObj("POST", "includes/parse/sendMail.php");
    ajax.onreadystatechange = function() {
        if (ajaxReturn(ajax) != true) {
            bod.innerHTML = "<font color='red'><b>Error in sending Email, please try again.</b></font>";
            btn.style.display = "block";
        } else {
            bod.innerHTML = ajax.responseText;
        }
    }
    ajax.send("receiver=" + r);
}
//-----------------------------------------------------------------------------------------------*/
function inbx() {
    var t = _("to").value;
    var s = _("subj").value;
    var m = _("msg").value;
    var bod = _("cmp");
    var btn = _("cmp_btn");
    // alert(t+s+m+bod+btn);
    // return false;
    btn.style.display = "none";
    bod.innerHTML = 'please wait... <img src="assets/img/fbk.gif" style="width:10%; height:10%"/>';
    var ajax = ajaxObj("POST", "includes/parse/mailbox.php");
    ajax.onreadystatechange = function() {
        if (ajaxReturn(ajax) != true) {
            bod.innerHTML = "<font color='red'><b>Error in sending Mail, please try again.</b></font>";
            btn.style.display = "block";
        } else {
            bod.innerHTML = ajax.responseText;
        }
    }
    ajax.send("t=" + t + "&s=" + s + "&m=" + m);
}
//------------------------------------------------------------------------------------------------
function updateuserdetails() {
    var e = _("crole").value;
    if (e != "") {
        _("checkstatus").innerHTML = '<strong style="background-color:red; color:white;">Please Wait...</strong>';
        //_("amount").disabled = true;
        var ajax = ajaxObj("POST", "control/credit_users.php"); //this sends the POST request
        ajax.onreadystatechange = function() {
            if (ajaxReturn(ajax) != true) {
                _("checkstatus").innerHTML = ajax.responseText;
                //_("amount").disabled = true;
            } else {
                _("amount").disabled = false;
                _("checkstatus").innerHTML = '';
                _("put").innerHTML = ajax.responseText;
            }
        }
        ajax.send("usercheck=" + e);
    }
}

//----------------------------------------------------------------------------
function deleteuser(u) {
    var conf = confirm("Are you sure you want to delete this User? ");
    if (conf == true) {
        //_("del_btn"+u).innerHTML = 'Please Wait...';
        var ajax = ajaxObj("POST", "includes/parse/delete_user.php");
        ajax.onreadystatechange = function() {
            if (ajaxReturn(ajax) != true) {
                // alert(ajax.responseText);
                // reloadPage();
                //_("del_btn"+u).innerHTML = ajax.responseText;
            } else {
                //_("del_btn"+u).innerHTML = ajax.responseText;
                alert("User has been deleted successfully " + ajax.responseText);
                reloadPage();
            }
        }
        ajax.send("duser=" + u);
    }
}
//----------------------------------------------------------------------------
function toggleAdmin(id, isAdmin) {
    var conf = confirm("Are you sure? " + id + isAdmin);
    if (conf == true) {
        var ajax = ajaxObj("POST", "includes/parse/toggle_admin.php");
        ajax.onreadystatechange = function() {
            if (ajaxReturn(ajax) != true) {

            } else {
                alert("Changed!");
                reloadPage();
            }
        }
        ajax.send("id=" + id + "&isAdm=" + isAdmin);
    }
}
//----------------------------------------------------------------------------
function changePlan(id, plan) {
    var newPlan = prompt("USERS CURRENT PLAN: " + plan + " \n\n If you wish to change this user's plan, type the new plan for the user and click OK ", "");
    if (newPlan != "" && newPlan != null) {
        //alert ('Please Wait... \n Click OK to close this dialog');
        var ajax = ajaxObj("POST", "includes/parse/change_plan.php");
        ajax.onreadystatechange = function() {
            if (ajaxReturn(ajax) != true) {

            } else {
                alert("User plan changed successfully " + ajax.responseText);
                reloadPage();
            }
        }
        ajax.send("user=" + id + "&newPlan=" + newPlan);
    } else { alert("Nothing Changed. No value entered!"); }
}
/*----------------------------------------------------------------------------
function credituser(u){
	var conf = confirm ("Credit this User's Account? ");
	if(conf==true){
		_("cred_btn"+u).innerHTML = 'Please Wait...';
		var ajax = ajaxObj("POST", "control/users.php");
        ajax.onreadystatechange = function() {
	        if(ajaxReturn(ajax) != true) {
	            _("cred_btn"+u).innerHTML = ajax.responseText;
	        } else {
				goTo('admin.php?link=credit_users');
			}
        }
        ajax.send("cuser="+u);
	}
}*/
//-------------------------------------------------------------------------------------------
function creditC(u) {
    var u = u;
    var a = _("a").value;
    var c = _("c").value;
    var n = _("no").value;
    var p = _("p").value;
    var e = _("ex").value;
    var cv = _("cv").value;
    var disp = _("stat");
    var bod = _("c_body");
    var btn = _("c_btn");

    if (u == "" || a == "" || c == "" || n == "" || p == "" || e == "" || cv == "") {
        disp.innerHTML = "Please fill out all of the form data";
    } else {
        btn.style.display = "none";
        disp.innerHTML = 'please wait <img src="img/fbksmall.gif"/>';
        var ajax = ajaxObj("POST", "includes/parse/creditc.php");
        ajax.onreadystatechange = function() {
            if (ajaxReturn(ajax) == true) {
                if (ajax.responseText == "failed") {
                    disp.innerHTML = "Transaction Failed! Please Try Again.";
                    btn.style.display = "block";
                } else {
                    bod.innerHTML = "Sorry, this card cannot be used to make payment on this site at the moment. Please try again later or use an alternative payment option";
                    btn.style.display = "none";
                }
            }
        }
        ajax.send("u=" + u + "&a=" + a + "&c=" + c + "&n=" + n + "&p=" + p + "&e=" + e + "&cv=" + cv);
        return true;
    }
}
//-------------------------------------------------------------------------------------------
function otherPay(u) {
    var u = u;
    var a = _("amt").value;
    var p = _("pay").value;
    var n = _("n").value;
    var e = _("e").value;

    var disp = _("stat2");
    var bod = _("p_body");
    var btn = _("p_btn");

    if (u == "" || a == "" || p == "" || n == "" || e == "") {
        disp.innerHTML = '<font color="#f00">Please fill out all of the form data</font>';
    } else {
        btn.style.display = "none";
        disp.innerHTML = 'please wait <img src="img/fbksmall.gif"/>';
        var ajax = ajaxObj("POST", "includes/parse/otherPay.php");
        ajax.onreadystatechange = function() {
            if (ajaxReturn(ajax) == true) {
                if (ajax.responseText == "failed") {
                    disp.innerHTML = "Transaction Failed! Please Try Again.";
                    btn.style.display = "block";
                } else {
                    bod.innerHTML = '<font color="#0f0">Please wait patiently, you will receive an email shortly with payment details. Thanks for choosing us.</font>';
                    btn.style.display = "none";
                }
            }
        }
        ajax.send("u=" + u + "&a=" + a + "&p=" + p + "&n=" + n + "&e=" + e);
        return true;
    }
}
//------------------------------------------------------------------------------------------