import { useEffect, useRef, useState } from "react";
import "../css/aio.css";
import api from "../api.js";
import { useNavigate } from "react-router-dom";

export const Header = ({ user, setUser }) => {
  const navigate = useNavigate();
  const logout = () => {
    const result = api.post("/auth/logout");
    console.log(result);
    setUser(null);
    navigate("/");
  };

  return (
    <header>
      <nav>
        <span>Slurppass.</span>
        {user == null ? (
          <a id="toppy" href="/login">
            Sign up/Log in
          </a>
        ) : (
          <p>
            welcome {user},{" "}
            <a
              onClick={() => {
                logout();
              }}
              id="toppy"
            >
              sign out!
            </a>
          </p>
        )}
      </nav>
    </header>
  );
};

export const Footer = () => {
  return (
    <footer>
      <p>this is a footer</p>
    </footer>
  );
};

export const Form = ({ user, setUser }) => {
  const [toggleLogin, setToggleLogin] = useState(false);
  const emailRef = useRef();
  const nameRef = useRef();
  const passwordRef = useRef();
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      navigate("/");
    }
  }, [user, navigate]);

  const login = async ({ email, password }) => {
    try {
      const result = await api.post("/auth/login", {
        email: email,
        password: password,
      });
      if (result.data.status_code === 403) {
        console.log(result.data);
      } else {
        console.log(result.data);
        setUser(result.data.user);
        navigate("/");
      }
    } catch (error) {
      console.log("error loggin in", error);
    }
  };

  const regsiter = async ({ name, email, password }) => {
    try {
      const result = await api.post("/auth/register", {
        name: name,
        email: email,
        password: password,
      });
      console.log(result.data);
      if (result.data.loggable == false) {
        return;
      } else {
        login({ email: email, password: password });
      }
    } catch (error) {
      console.log("error loggin in", error);
    }
  };

  const onSubmit = (e) => {
    e.preventDefault();
    if (!toggleLogin) {
      login({
        email: emailRef.current.value,
        password: passwordRef.current.value,
      });
    } else {
      regsiter({
        name: nameRef.current.value,
        email: emailRef.current.value,
        password: passwordRef.current.value,
      });
    }
  };

  return (
    <form onSubmit={onSubmit}>
      <h3>{!toggleLogin ? "Login" : "Register"}</h3>
      {!toggleLogin ? null : (
        <input
          type="text"
          name="name"
          placeholder="Name"
          ref={nameRef}
          required
        />
      )}
      <input
        type="email"
        name="email"
        placeholder="email"
        ref={emailRef}
        required
      />
      <input
        type="password"
        name="password"
        minLength={8}
        maxLength={15}
        placeholder="password"
        ref={passwordRef}
        required
      />
      {!toggleLogin ? (
        <a
          onClick={() => {
            setToggleLogin(true);
          }}
        >
          New user? Sign up!
        </a>
      ) : (
        <a
          onClick={() => {
            setToggleLogin(false);
          }}
        >
          Existing User? Log in!
        </a>
      )}
      <button type="submit">less go.</button>
    </form>
  );
};
