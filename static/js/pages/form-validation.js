$(document).ready(function() {
    // Generate a simple captcha
    function randomNumber(min, max) {
        return Math.floor(Math.random() * (max - min + 1) + min);
    };
    $('#captchaOperation').html([randomNumber(1, 20), '+', randomNumber(1, 30), '='].join(' '));
	
	
	//EXAMPLE REGISTER FORM
    $('#registerForm').bootstrapValidator({
        message: 'This value is not valid',
        fields: {
            nombres: {
                message: 'El texto ingresado no es valido',
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    },
                    stringLength: {
                        min: 1,
                        max: 30,
                        message: 'Este campo debe ser mayor de 6 y menos de 30 caracteres de longitud'
                    },
                }
            },
            apellidos: {
                message: 'El texto ingresado no es valido',
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    },
                    stringLength: {
                        min: 1,
                        max: 30,
                        message: 'Este campo debe ser mayor de 6 y menos de 30 caracteres de longitud'
                    },
                }
            },
            username: {
                message: 'El nombre de usuario no es valido',
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    },
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: 'Este campo debe ser mayor de 6 y menos de 30 caracteres de longitud'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z0-9_]+$/,
                        message: 'Solo caracteres alfanumericos y guiones bajos'
                    },
                }
            },
            correo: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    },
                    emailAddress: {
                        message: 'El correo ingresado no es valido'
                    }
                }
            },
            fecha_nacimiento: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    }
                }
            },
            fecha: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    }
                }
            },
            password: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    },
                    identical: {
                        field: 'confirmPassword',
                        message: 'La contraseña y su confirmación no son iguales'
                    }
                }
            },
            confirmPassword: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    },
                    identical: {
                        field: 'password',
                        message: 'La contraseña y su confirmación no son iguales'
                    }
                }
            },
            tipo_doc: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    }
                }
            },
            almacen: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    }
                }
            },
            departamento: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    }
                }
            },
            facebook: {
                validators: {
                    regexp: {
                        regexp: /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \?=.-]*)*\/?$/ ,
                        message: 'La URL ingresada no es valida'
                    },
                }
            },
            pagina_web: {
                validators: {
                    regexp: {
                        regexp: /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \?=.-]*)*\/?$/ ,
                        message: 'La URL ingresada no es valida'
                    },
                }
            },
            twitter: {
                validators: {
                    regexp: {
                        regexp: /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \?=.-]*)*\/?$/ ,
                        message: 'La URL ingresada no es valida'
                    },
                }
            },
            ciudad: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    }
                }
            },
            direccion: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    }
                }
            },
            categoria: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    },
                    regexp: {
                        regexp: /^[0-9]+$/,
                        message: 'Favor seleccione una categoria valida'
                    },
                }
            },
            nombre: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    }
                }
            },
            fecha_inicio: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    }
                }
            },
            fecha_fin: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    }
                }
            },
            local: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    }
                }
            },
            genero: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    }
                }
            },
            estado_civil: {
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    }
                }
            },
            hora: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        }
                    }
                },
            hora_inicio: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        }
                    }
                },
            hora_fin: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        }
                    }
                },
            documento: {
                message: 'El documento no es valido',
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    },
                    stringLength: {
                        min: 5,
                        max: 11,
                        message: 'Este campo debe tener mínimo 5 caracteres y máximo 15'
                    },
                }
            },
            grupo: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        }
                    }
                },
            telefono: {
                message: 'El telefono no es valido',
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    },
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: 'Este campo debe tener mínimo 5 caracteres'
                    },
                }
            },
            valor_boleta: {
                message: 'El valor no es valido',
                validators: {
                    notEmpty: {
                        message: 'Este campo es requerido'
                    },
                    stringLength: {
                        min: 4,
                        max: 8,
                        message: 'Este campo debe tener mínimo 4 caracteres'
                    },
                    regexp: {
                        regexp: /^[0-9]+$/,
                        message: 'Solo numeros'
                    },
                }
            },
            captcha: {
                validators: {
                    callback: {
                        message: 'Respuesta incorrecta',
                        callback: function(value, validator) {
                            var items = $('#captchaOperation').html().split(' '), sum = parseInt(items[0]) + parseInt(items[2]);
                            return value == sum;
                        }
                    }
                }
            }
        }
    });
	
	
	$(".registerForm").each(function(index, el) {
        //EXAMPLE REGISTER FORM
        $(this).bootstrapValidator({
            message: 'This value is not valid',
            fields: {
                nombres: {
                    message: 'El texto ingresado no es valido',
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        },
                        stringLength: {
                            min: 1,
                            max: 30,
                            message: 'Este campo debe ser mayor de 6 y menos de 30 caracteres de longitud'
                        },
                    }
                },
                apellidos: {
                    message: 'El texto ingresado no es valido',
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        },
                        stringLength: {
                            min: 1,
                            max: 30,
                            message: 'Este campo debe ser mayor de 6 y menos de 30 caracteres de longitud'
                        },
                    }
                },
                almacen: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        }
                    }
                },
                correo: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        },
                        emailAddress: {
                            message: 'El correo ingresado no es valido'
                        }
                    }
                },
                fecha_nacimiento: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        }
                    }
                },
                password: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        },
                        identical: {
                            field: 'confirmPassword',
                            message: 'La contraseña y su confirmación no son iguales'
                        }
                    }
                },
                confirmPassword: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        },
                        identical: {
                            field: 'password',
                            message: 'La contraseña y su confirmación no son iguales'
                        }
                    }
                },
                tipo_doc: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        }
                    }
                },
                departamento: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        }
                    }
                },
                facebook: {
                    validators: {
                        regexp: {
                            regexp: /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \?=.-]*)*\/?$/ ,
                            message: 'La URL ingresada no es valida'
                        },
                    }
                },
                pagina_web: {
                    validators: {
                        regexp: {
                            regexp: /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \?=.-]*)*\/?$/ ,
                            message: 'La URL ingresada no es valida'
                        },
                    }
                },
                twitter: {
                    validators: {
                        regexp: {
                            regexp: /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \?=.-]*)*\/?$/ ,
                            message: 'La URL ingresada no es valida'
                        },
                    }
                },
                ciudad: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        }
                    }
                },

                direccion: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        }
                    }
                },
                categoria: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        },
                        regexp: {
                            regexp: /^[0-9]+$/,
                            message: 'Favor seleccione una categoria valida'
                        },
                    }
                },
                nombre: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        }
                    }
                },
                fecha_inicio: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        }
                    }
                },
                fecha_fin: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        }
                    }
                },
                local: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        }
                    }
                },
                genero: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        }
                    }
                },
                estado_civil: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        }
                    }
                },
                hora: {
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        }
                    }
                },
                documento: {
                    message: 'El documento no es valido',
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        },
                        stringLength: {
                            min: 5,
                            max: 11,
                            message: 'Este campo debe tener mínimo 5 caracteres y máximo 11'
                        },
                    }
                },
                telefono: {
                    message: 'El telefono no es valido',
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        },
                        stringLength: {
                            min: 6,
                            max: 30,
                            message: 'Este campo debe tener mínimo 5 caracteres'
                        },
                    }
                },
                valor_boleta: {
                    message: 'El valor no es valido',
                    validators: {
                        notEmpty: {
                            message: 'Este campo es requerido'
                        },
                        stringLength: {
                            min: 4,
                            max: 8,
                            message: 'Este campo debe tener mínimo 4 caracteres'
                        },
                        regexp: {
                            regexp: /^[0-9]+$/,
                            message: 'Solo numeros'
                        },
                    }
                },
                captcha: {
                    validators: {
                        callback: {
                            message: 'Respuesta incorrecta',
                            callback: function(value, validator) {
                                var items = $('#captchaOperation').html().split(' '), sum = parseInt(items[0]) + parseInt(items[2]);
                                return value == sum;
                            }
                        }
                    }
                }
            }
        });
    });
	
});