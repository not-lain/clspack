import inspect
import os
import warnings

def pack(cls, out_folder="package"):
    """a function to inspect a class that was defined in __main__
    Args:
      cls = takes the class

    important :
    to get the class from a variable that was created you can use
    f.__class__.mro()

    """
    global cls_to_file
    cls_name = str(cls.mro()[0])[17:-2]
    for key, value in cls.__dict__.items():
        if key == "__module__":
            if value != "__main__":
                # case class not defined in __main__ so no need to complete
                # we can import the class directly from its file
                # TODO: create the other function
                raise NotImplementedError(f"""class {cls_name} not defined in __main__
                                        and we did not support this feature yet
                                        any contributions are welcome at https://github.com/not-lain/clspack""")

            else:
                cls_to_file = ""
                # TODO: check if none of the inhereted methods belong to __main__ too
                inheretances = [str(i)[8:-2] for i in cls.mro()[1:-1]]
                for i, ancestor in enumerate(inheretances):
                    index = len(ancestor) - ancestor[::-1].index(".") - 1
                    print(ancestor[:index], ancestor[index + 1 :])
                    module, inheretances[i] = ancestor[:index], ancestor[index + 1 :]
                    if "__main__" not in module:
                        # for cases where we are inheriting from other classes that are defined in __main__
                        cls_to_file += f"from {module} import {inheretances[i]}\n"
                        #TODO: check if the the module is already imported in the cls_to_file
                        # to cleanup for cases that the import is written in different line such as this one :
                        # from transformers import AutoModelForXXX
                        # from transformers import PushToHubMixin
                    else : 
                        warnings.warn(f"""the class {inheretances[i]} was defined in __main__
                                      and we did not support when there are inheritances that are defined in __main__ yet
                                      any contributions are welcome at https://github.com/not-lain/clspack""")
                inheretances = ",".join(inheretances)
                cls_to_file += f"class {cls_name}({inheretances}):\n"
        elif key == "__doc__":
            cls_to_file += "  " + repr(value) + "\n"
        else:
            try:
                # try to get the function/method code
                # or a class attribute
                st = f"{cls_name}.{key}"
                source_code = inspect.getsource(eval(st))
                cls_to_file += source_code + "\n"
            except:  # noqa: E722
                 # hidden magic methods that were not specified
                  # cls_to_file += "  " + key + " = " + repr(value) + "\n"
                  pass
    with open(os.path.join(out_folder,"__init__.py"),"w") as f : 
        f.write("")
    with open(os.path.join(out_folder,"architecture.py"),"w") as f:
        f.write(cls_to_file)
