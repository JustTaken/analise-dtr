using CSV
using CairoMakie
using DataFrames
using StatsBase

# Heuristics:
#   The data starts at the same time that the mapping function starts,
#   therefore, caution has to be taken when writing down the data to
#   csv format, because if the experimental data has some delay before
#   it starts having the expected behaviour byt the parameterized function 

A = 1.0
B = 0.5
C = 0.5
Delta = 0.5

const Param = Vector{Number}

function convert_current(in_current::Float64)
    return in_current * 1.4 + 0.5
end

function load_data(file)
    data = DataFrame(CSV.File(file, header=1))

    y = convert_current.(data[!, "Current"])
    l = length(y)

    m = mean(y[l - Int64(round(l / 10)):l])
    y = y .- m
    x = collect(0:l - 1)

    x, y, m
end

function f(p::Param, x::Vector{<:Number})::Vector{<:Number}
    p[1] .* exp.(.- p[2] .* x) .- p[1] .* exp.(.- p[3] .* x)
end

function data_integral(x::Vector{<:Number}, y::Vector{<:Number})::Number
    let sum = 0
        for i in range(2, length(x))
            sum += (y[i] + y[i - 1]) * (x[i] - x[i - 1]) * 0.5
        end

        sum
    end
end

function rest(y_hat::Vector{<:Number}, y::Vector{<:Number})::Vector{<:Number}
    (y .- y_hat) .^ 2
end

function test_interval(b::Number, c::Number, delta::Number, len::Int64)
    b_vec = collect(range(b - delta, b + delta, length = len))
    c_vec = collect(range(c - delta, c + delta, length = len))

    b_vec, c_vec
end

function find_min_sse_coeficients(x::Vector{<:Number}, y::Vector{<:Number})
    data = data_integral(x, y)
    base_length::Int64 = 100

    let minimum = 1000, min_b = B, min_c = C, min_a = A, delta = Delta
        for r in range(1, 4)
            b, c = test_interval(min_b, min_c, delta, base_length)
            delta = delta / base_length

            for j in range(1, length(b))
                for i in range(1, length(c))
                    a = get_integral_ratio(b[j], c[i], x[1], x[length(x)], data)
                    sse = sum(rest(f(Param([a, b[j], c[i]]), x), y))

                    if sse < minimum
                        minimum = sse
                        min_b = b[j]
                        min_c = c[i]
                        min_a = a
                    end
                end
            end
        end

        minimum, min_a, min_b, min_c
    end
end

function find_fit(x::Vector{<:Number}, y::Vector{<:Number})
    m, A, B, C = find_min_sse_coeficients(x, y)
    p = Param([A, B, C]) 

    f(p,  x), p, m
end

function integral(a::Number, b::Number, c::Number, s::Number, e::Number)::Number
    a * ((exp(-b * s) - exp(-b * e)) / b + (exp(-c * e) - exp(-c * s)) / c)
end

function get_integral_ratio(b::Number, c::Number, s::Number, e::Number, data::Number)::Number
    parameterized = integral(1.0, b, c, s, e)

    data / parameterized
end

function t_mean(a::Number, b::Number, c::Number)
    return (b * c) / (b - c) * (1 / c^2 - 1 / b^2)
end

function parameters(a::Number, b::Number, c::Number)
    tm = t_mean(a, b, c)

    fac1 = (b * c) / (b - c)
    fac2 = tm^2 / c - (2 * tm) / c^2 + 2 / c^3 - tm^2 / b + (2 * tm) / b^2 - 2 / b^3

    return tm, fac1 * fac2
end

function rd(x)
    return round(x, digits=2)
end

function add_data_to_figure(path, fig, row, col)
    x, y, m = load_data(path)
    fit, param, r = find_fit(x, y)

    a = param[1]
    b = param[2]
    c = param[3]

    tm, var = parameters(a, b, c)
    n = tm^2 / var

    println(path, " := A(", rd(a), "), B(", rd(b), "), C(", rd(c), "), tm(", rd(tm), "), var(", rd(var), "), n(", rd(n), "), resto(", rd(r), ")")

    ax = Axis(fig[row, col])
    scatter!(ax, x, y, color = :orange, markersize=4)
    scatter!(ax, x, fit, color = :red, markersize=4)
end

function plot_file(path)
    fig = Figure()
    add_data_to_figure(path, fig, 1, 1)
    fig
end

function plot_dir(path::String, columns::Int64)
    fig = Figure()

    let row = 1, col = 1
        for f in readdir(path)
            if col > columns
                col = 1
                row += 1
            end

            add_data_to_figure(joinpath(path , f), fig, row, col)
            col += 1
        end
    end

    fig
end
