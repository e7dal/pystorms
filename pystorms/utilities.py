import numpy as np
import os
import platform

# Local Path
HERE = os.path.abspath(os.path.dirname(__file__))


def load_network(name):
    r""" returns the path to the desired network.

    Parameters
    ----------
    name : str
        name of the network. *alpha*, *beta*, *gamma*, *epsilon* and *delta* are valid
        keywords

    Returns
    -------
    path : str
        path to the network
    """
    if name == "alpha":
        path = os.path.join(HERE, "networks/alpha.inp")
    elif name == "beta":
        path = os.path.join(HERE, "networks/beta.inp")
    elif name == "delta":
        path = os.path.join(HERE, "networks/delta.inp")
    elif name == "epsilon":
        path = os.path.join(HERE, "networks/epsilon.inp")
    elif name == "gamma":
        path = os.path.join(HERE, "networks/gamma.inp")
    elif name == "theta":
        path = os.path.join(HERE, "networks/theta.inp")
    else:
        raise ValueError("Undefined Network, please refer to the documentation")
    return path


def load_binary(name):
    r""" returns specified swmm binary based on the operating system.

    Parameters
    ----------
    name : str
        name of the binary. refer to the documentation for the key words

    Returns
    -------
    path : str
        path to the binary
    """
    # Find the path to the library
    op_system = platform.system()
    if op_system == "Linux":
        path = "/linux/libswmm5.so"
    elif op_system == "Windows":
        path = "/windows/swmm5.dll"
    elif op_system == "Darwin":
        path = "/macos/libswmm5.so"
    else:
        raise ValueError(
            "Operating system not identified, please check the binary path or overwrite it. \
                    Refer to the documentation for additional details."
        )

    # Choose the binary
    if name == "pollutant_support":
        path = "binaries/" + name + path
        path = os.path.join(HERE, path)
    else:
        raise ValueError(
            "binaries not found. Refer to the documentation for the list avaiable binaries"
        )

    return path


def append_rainfall(
    network_source,
    rainfall_source,
    destination="./temp_network.inp",
    event_name="TestRain",
):
    r"""

    Appends rainfall timeseries from a pandas time series to the swmm input file by creating
    a new copy of the network.

    Parameters
    ----------
    network_source
        Path to swmm input file
    rainfall_source
        Pandas.Series of timestamped rainfall
    destination
        Path to make the copy of the swmm file
    event_name
        Name of the Event

    Returns
    -------
    path
        Path to the swmm inp file with Rainfall
    """
    path_to_file = destination
    with open(network_source) as source:
        with open(path_to_file, "w") as destination:
            for line in source:
                destination.write(line)
            destination.write("\n")
            destination.write("[TIMESERIES] \n")
            destination.write(";;Name           Date       Time       Value \n")
            destination.write(";;-------------- ---------- ---------- ---------- \n")
            for i in range(0, len(rainfall_source)):
                destination.write(
                    "{0: <14}   {1}/{2}/{3:<6} {4}:{5}:{6: <3}   {7} \n".format(
                        event_name,
                        rainfall_source.index[i].month,
                        rainfall_source.index[i].day,
                        rainfall_source.index[i].year,
                        rainfall_source.index[i].hour,
                        rainfall_source.index[i].minute,
                        rainfall_source.index[i].second,
                        rainfall_source[i],
                    )
                )
    return path_to_file


def perf_metrics(performance_measure, metric):
    r"""

    Compute the performance statistics for the performance metrics

    Parameters
    ----------
    performance_measure
        data whose stats have to be computed
    metric
        stat to be computed

    Returns
    -------
    stat
        desired metric for data

    """

    if len(performance_measure) < 1:
        raise ValueError("Run step; performance metrics have not been computed")
    if metric == "mean":
        return sum(performance_measure) / len(performance_measure)
    elif metric == "cumulative":
        return sum(performance_measure)
    elif metric == "median":
        return np.median(performance_measure)
    elif metric == "maximum":
        return np.max(performance_measure)
    elif metric == "minimum":
        return np.min(performance_measure)
    elif metric == "recent":
        return performance_measure[-1]
    else:
        raise ValueError(
            "mean, cumulative,median, maximum, minimum, and recent are the only valid metrics"
        )


def threshold(value, target=0.10, scaling=1.0):
    r"""

    measure the deviation from flow

    Parameters
    ----------
    value
        value whose diviation should be measured
    target
        threshold value
    scaling
        scaling factor

    Returns
    -------
    performace
        diviation scale

    """
    performance = 0.0
    if value <= target:
        performance += 0.0
    else:
        performance += (value - target) * scaling
    return performance
